import os
import glob
from junitparser import JUnitXml, TestSuite

def aggregate_junit_reports(report_dir, output_report):
    aggregated = JUnitXml()
    aggregated.name = "Aggregated Tests"

    for file_path in glob.glob(os.path.join(report_dir, "**/report.xml"), recursive=True):
        xml = JUnitXml.fromfile(file_path)
        for suite in xml:
            if isinstance(suite, TestSuite):
                aggregated.add_testsuite(suite)

    aggregated.write(output_report)
    print(f"Aggregated report saved to {output_report}")

if __name__ == "__main__":
    import os
    report_dir = os.getenv("REPORT_DIR", "./junit-reports")
    output_report = os.getenv("OUTPUT_FILE", "aggregated-report.xml")
    aggregate_junit_reports(report_dir, output_report)

