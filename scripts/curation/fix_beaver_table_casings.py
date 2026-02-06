#
# Copyright IBM Corp. 2025 - 2026
# SPDX-License-Identifier: Apache-2.0
#

import json
import re
import sys


def uppercase_table_names(json_file_path, output_file_path=None):
    """
    Replace table names in SQL queries with their uppercase versions.

    Args:
        json_file_path (str): Path to the input JSON file
        output_file_path (str): Path to save the modified JSON file (optional)
    """

    # List of table names to convert to uppercase
    table_names = [
        "academic_terms",
        "academic_terms_all",
        "academic_term_parameter",
        "buildings",
        "cip",
        "cip_with_version",
        "cis_course_catalog",
        "cis_hass_attribute",
        "course_catalog_subject_offered",
        "drupal_course_catalog",
        "drupal_employee_directory",
        "employee_directory",
        "estimated_surcharges_estonly",
        "fac_building",
        "fac_building_address",
        "fac_floor",
        "fac_major_use",
        "fac_organization",
        "fac_rooms",
        "fclt_building",
        "fclt_building_address",
        "fclt_building_address_hist",
        "fclt_building_hist",
        "fclt_building_hist_1",
        "fclt_floor",
        "fclt_floor_hist",
        "fclt_major_use",
        "fclt_major_use_hist",
        "fclt_organization",
        "fclt_organization_hist",
        "fclt_org_dlc_key",
        "fclt_rooms",
        "fclt_rooms_hist",
        "frc_fiscal_periods",
        "fund_center_hierarchy",
        "hr_faculty_roster",
        "hr_org_unit",
        "hr_org_unit_new",
        "iap_subject_category",
        "iap_subject_detail",
        "iap_subject_person",
        "iap_subject_session",
        "iap_subject_sponsor",
        "ir_institution",
        "library_course_instructor",
        "library_material_status",
        "library_reserve_catalog",
        "library_reserve_matrl_detail",
        "library_subject_offered",
        "master_dept_dcode_parent",
        "master_dept_hierarchy",
        "master_dept_hierarchy_links",
        "mit_holiday_closing_calendar",
        "mit_student_directory",
        "moira_list",
        "moira_list_detail",
        "moira_list_owner",
        "opa_person_current",
        "person_auth_area",
        "profit_center_group",
        "roles_fin_pa",
        "se_person",
        "sis_admin_department",
        "sis_course_description",
        "sis_department",
        "sis_lookup",
        "sis_subject_code",
        "sis_term_address_category",
        "space_detail",
        "space_floor",
        "space_supervisor_usage",
        "space_unit",
        "space_unit2",
        "space_usage",
        "student_degree_program",
        "student_department",
        "student_ethnic_subgroup",
        "subject_attribute",
        "subject_enrollable",
        "subject_grouping",
        "subject_iap_schedule",
        "subject_offered",
        "subject_offered_summary",
        "subject_selector",
        "subject_summary",
        "time_day",
        "time_month",
        "time_quarter",
        "tip_detail",
        "tip_material",
        "tip_material_status",
        "tip_subject_offered",
        "top_level_domain",
        "warehouse_users",
        "zip_canada",
        "zip_usa",
        "zpm_rooms_load",
    ]

    # Sort table names by length (descending) to avoid partial replacements
    table_names_sorted = sorted(table_names, key=len, reverse=True)

    # Read the JSON file
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{json_file_path}'.")
        return

    def process_sql_content(sql_content):
        """Process a single SQL string and replace table names with uppercase versions."""
        for table_name in table_names_sorted:
            # Use word boundaries to ensure we only replace complete table names
            # This pattern matches the table name when it's:
            # - At the beginning/end of string or surrounded by non-word characters
            # - Case insensitive matching
            pattern = r"\b" + re.escape(table_name) + r"\b"
            sql_content = re.sub(
                pattern, table_name.upper(), sql_content, flags=re.IGNORECASE
            )
        return sql_content

    # Process each object in the array
    for obj in data:
        if "sql" in obj and obj["sql"]:
            if isinstance(obj["sql"], list):
                # Handle array of SQL statements
                processed_sql_array = []
                for sql_statement in obj["sql"]:
                    if isinstance(sql_statement, str):
                        processed_sql_array.append(process_sql_content(sql_statement))
                    else:
                        # Keep non-string items as-is
                        processed_sql_array.append(sql_statement)
                obj["sql"] = processed_sql_array
            elif isinstance(obj["sql"], str):
                # Handle single SQL string
                obj["sql"] = process_sql_content(obj["sql"])
            # If sql is neither string nor list, leave it unchanged

    # Determine output file path
    if output_file_path is None:
        # Use the same file path to overwrite the original file
        output_file_path = json_file_path

    # Write the modified data back to file
    try:
        with open(output_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Successfully processed and saved to: {output_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")


# Example usage
if __name__ == "__main__":
    # Check if filename is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python fix_beaver_table_casings.py <json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Overwrite the original file
    uppercase_table_names(input_file)
