import openpyxl
from services.models import AllowedVehicles


# load data from excel file and save it to the database
def import_vehicles_from_excel(file_path):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Iterate through the rows in the sheet
    for row in sheet.iter_rows(min_row=2, values_only=True):
        owner = row[0]
        categ = row[1]
        identification_nr = row[2]
        zona = row[3]
        nr_aviz = row[4]
        data_inceput = row[5]
        data_sfarsit = row[6]
        descriere = row[7]


        # Create a new AllowedVehicles object
        new_vehicle = AllowedVehicles(
            owner=owner,
            categ=categ,
            identification_nr=identification_nr,
            zona=zona,
            nr_aviz=nr_aviz,
            data_inceput=data_inceput,
            data_sfarsit=data_sfarsit,
            descriere=descriere,
        )
        new_vehicle.save()
    # Close the workbook
    workbook.close()
    # Return the number of activities imported
    return f"Imported {sheet.max_row - 1} activities from {file_path}"