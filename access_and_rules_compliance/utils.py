import openpyxl
from services.models import AllowedVehicles


# load data from excel file and save it to the database
def import_vehicles_from_excel(file_path):
    from services.models import VehicleCategory
    from datetime import datetime

    def parse_excel_date(value):
        if isinstance(value, datetime):
            return value.date()
        try:
            return datetime.strptime(str(value), '%Y-%m-%d').date()
        except Exception:
            return None

    errors = []
    success_count = 0

    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Iterate through the rows in the sheet
    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        try:
            owner = row[0]
            categ_title = row[1]
            identification_nr = row[2]
            zona = row[3]
            nr_aviz = row[4]
            data_inceput = parse_excel_date(row[5])
            data_sfarsit = parse_excel_date(row[6])
            descriere = row[7]

            # Get or create the vehicle category
            category = VehicleCategory.objects.filter(title__iexact=categ_title).first()
            if not category:
                raise ValueError(f"Unknown category '{categ_title}'")

            # Create a new AllowedVehicles object
            AllowedVehicles.objects.create(
                owner=owner,
                categ=category,
                identification_nr=identification_nr,
                zona=zona,
                nr_aviz=nr_aviz,
                data_inceput=data_inceput,
                data_sfarsit=data_sfarsit,
                descriere=descriere,
            )
            success_count += 1
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")
    # Close the workbook
    workbook.close()
    # Return the number of activities imported
    if errors:
        return f"Imported {success_count} vehicles with errors:\n" + "\n".join(errors)
    return f"Successfully imported {success_count} vehicles."