import csv


def get_state_school_id(disctrict_id, school_id):
    return "VA-{:03d}-{:03d}{:04d}".format(disctrict_id, disctrict_id, school_id)

with open('SOL pass rate subject wise with state school id.csv', mode='w') as write_file:
    with open('SOL pass rate subject wise.csv', newline='') as read_file:
        filereader = csv.DictReader(read_file)
        fieldnames = filereader.fieldnames + ['State School ID']
        filewriter = csv.DictWriter(write_file, fieldnames=fieldnames)
        filewriter.writeheader()
        for row in filereader:
            row['State School ID'] = get_state_school_id(int(row['Division Number']), int(row['School Number']))
            filewriter.writerow(row)







