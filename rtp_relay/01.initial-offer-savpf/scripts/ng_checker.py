#!/usr/bin/env python3
"""GH-3902 rtp_relay checker -- assert what OpenSIPS ASKS rtpengine.

Dependency-free (stdlib only, no tshark/scapy): parses a tcpdump pcap and decodes
the rtpengine "ng" bencode control messages. The bug (#3902): the callee/WebRTC
profile provisioned in the branch_route is not linked into sess->legs[CALLEE]
before the offer, so rtp_relay asks rtpengine for plain RTP/AVP -- losing
UDP/TLS/RTP/SAVPF + ICE=force. We read the ng OFFER/ANSWER on udp:<ng_port> and
assert the profile is present.

  ng_checker.py <pcap> savpf [--ng-port N]
        PASS iff some OFFER carries UDP/TLS/RTP/SAVPF + ICE=force.
  ng_checker.py <pcap> count <min_offers> [offer|answer] [--ng-port N]
        PASS iff >= min_offers OFFERs AND every msg of that axis keeps SAVPF.
  ng_checker.py <pcap> failover --mi-port M [--ng-port N]
        PASS iff a re-anchor OFFER/ANSWER after the rtp_relay_update MI keeps SAVPF.

Exit 0 = PASS, non-zero = FAIL.
"""
import struct
import sys

WANT_PROTO = b"UDP/TLS/RTP/SAVPF"
WANT_ICE = b"force"
DEFAULT_NG_PORT = 22222


def read_pcap(path):
    """Yield (ts_relative, linktype, frame) per record of a classic pcap."""
    with open(path, "rb") as f:
        gh = f.read(24)
        if len(gh) < 24:
            return
        magic = gh[:4]
        if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
            endian = "<"
        elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
            endian = ">"
        else:
            raise SystemExit("not a classic pcap (magic=%r); use tcpdump default "
                             "output, not pcapng" % magic)
        nanos = magic in (b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d")
        linktype = struct.unpack(endian + "I", gh[20:24])[0]
        t0 = None
        while True:
            rh = f.read(16)
            if len(rh) < 16:
                return
            ts_sec, ts_frac, caplen, _orig = struct.unpack(endian + "IIII", rh)
            data = f.read(caplen)
            if len(data) < caplen:
                return
            ts = ts_sec + (ts_frac / 1e9 if nanos else ts_frac / 1e6)
            if t0 is None:
                t0 = ts
            yield (ts - t0, linktype, data)


def udp_payloads(path):
    """Yield (ts, dst_port, payload) for each IPv4/UDP packet."""
    for ts, linktype, data in read_pcap(path):
        if linktype == 1:                      # Ethernet (tcpdump -i osbr0)
            if len(data) < 14 or struct.unpack("!H", data[12:14])[0] != 0x0800:
                continue
            off = 14
        elif linktype == 113:                  # Linux cooked
            if len(data) < 16 or struct.unpack("!H", data[14:16])[0] != 0x0800:
                continue
            off = 16
        else:
            continue
        ip = data[off:]
        if len(ip) < 20 or (ip[0] >> 4) != 4 or ip[9] != 17:   # IPv4 + UDP
            continue
        udp = ip[(ip[0] & 0x0F) * 4:]
        if len(udp) < 8:
            continue
        yield (ts, struct.unpack("!H", udp[2:4])[0], udp[8:])


def command_of(msg):
    """Extract the bencode 7:command value (e.g. 'offer'/'answer') or None."""
    i = msg.find(b"7:command")
    if i < 0:
        return None
    colon = msg.find(b":", i + 9)
    if colon < 0:
        return None
    try:
        n = int(msg[i + 9:colon])
    except ValueError:
        return None
    return msg[colon + 1:colon + 1 + n].decode("latin1")


def ng_requests(path, ng_port):
    """[(ts, payload)] for ng requests sent TO rtpengine."""
    return [(ts, p) for ts, dport, p in udp_payloads(path)
            if dport == ng_port and b"7:command" in p]


def mi_time(path, mi_port):
    """Relative time of the rtp_relay_update MI request, or None."""
    for ts, dport, p in udp_payloads(path):
        if dport == mi_port and b"rtp_relay_update" in p:
            return ts
    return None


def fail(msg):
    print("FAIL: " + msg)
    return 1


def check_savpf(reqs):
    offers = [m for _t, m in reqs if command_of(m) == "offer"]
    print("ng requests: %d, OFFERs: %d" % (len(reqs), len(offers)))
    if not offers:
        return fail("no OFFER ng message captured -- harness/capture problem")
    if any(WANT_PROTO in m for m in offers) and any(WANT_ICE in m for m in offers):
        print("PASS: OFFER carries UDP/TLS/RTP/SAVPF + ICE=force")
        return 0
    return fail("OFFER missing the callee transcode-to profile -> proxy asked "
                "rtpengine for plain RTP/AVP -> WebRTC UA would 488 (#3902)")


def check_count(reqs, want, where):
    cmds = [(m, command_of(m)) for _t, m in reqs]
    offers = [m for m, c in cmds if c == "offer"]
    target = [m for m, c in cmds if c == ("answer" if where == "answer" else "offer")]
    savpf = [m for m in target if WANT_PROTO in m]
    print("OFFERs: %d (want >= %d), %s carrying SAVPF: %d/%d"
          % (len(offers), want, where, len(savpf), len(target)))
    if len(offers) < want:
        return fail("only %d/%d offers -> a re-INVITE did not re-anchor"
                    % (len(offers), want))
    if not target or len(savpf) != len(target):
        return fail("%d/%d %s msg(s) lost the WebRTC profile -> #3902 present"
                    % (len(target) - len(savpf), len(target), where))
    print("PASS: re-anchored AND all %d %s msg(s) kept UDP/TLS/RTP/SAVPF"
          % (len(target), where))
    return 0


def check_failover(reqs, t0):
    if t0 is None:
        return fail("no rtp_relay_update MI request seen on the MI port")
    msgs = [(command_of(m), WANT_PROTO in m) for t, m in reqs
            if t >= t0 and command_of(m) in ("offer", "answer")]
    print("MI fired at t=%.2fs, re-anchor offer/answer: %d" % (t0, len(msgs)))
    if not msgs:
        return fail("rtp_relay_update generated no re-anchor offer/answer")
    if not any(s for _c, s in msgs):
        return fail("failover re-anchor lost the WebRTC profile (all RTP/AVP) "
                    "-> WebRTC node would 488 the re-INVITE -> #3902 present")
    print("PASS: failover re-anchor preserved UDP/TLS/RTP/SAVPF")
    return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    pcap, mode, rest = argv[1], argv[2], argv[3:]
    ng_port, mi_port, pos, i = DEFAULT_NG_PORT, None, [], 0
    while i < len(rest):
        if rest[i] == "--ng-port":
            ng_port = int(rest[i + 1]); i += 2
        elif rest[i] == "--mi-port":
            mi_port = int(rest[i + 1]); i += 2
        else:
            pos.append(rest[i]); i += 1

    print("GH-3902 rtp_relay ng checker  mode=%s  ng-port=%d" % (mode, ng_port))
    reqs = ng_requests(pcap, ng_port)
    if mode == "savpf":
        return check_savpf(reqs)
    if mode == "count":
        if not pos:
            return fail("count mode needs <min_offers>")
        return check_count(reqs, int(pos[0]), pos[1] if len(pos) > 1 else "offer")
    if mode == "failover":
        if mi_port is None:
            return fail("failover mode needs --mi-port N")
        return check_failover(reqs, mi_time(pcap, mi_port))
    return fail("unknown mode %r" % mode)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
