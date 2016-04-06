import argparse

import xml.etree.ElementTree as ET

from Evtx.Evtx import Evtx
from Evtx.Views import _build_record_xml

def parse_evtx(filename, target_event_ids):
    """
    Parse .evtx file and output information about events whose event_id
    is in @target_event_ids.
    """

    columns = (
        'EventID', 'TimeCreated', 'IpAddress', 'IpPort', 'WorkstationName'
    )
    with Evtx(filename) as e:
        ret = []
        for record in e.records():
            xml = _build_record_xml(record)
            root = ET.fromstring(xml)
            event_id = time_created = None
            ip_address = ip_port = workstation_name = None
            for child in root.iter():
                if child.tag.find('EventID') != -1:
                    event_id = int(child.text)
                elif child.tag.find('TimeCreated') != -1:
                    try:
                        time_created = child.attrib['SystemTime']
                    except KeyError:
                        pass
                elif child.tag.find('Data') != -1:
                    try:
                        col = child.attrib['Name']
                        if col == 'IpAddress':
                            ip_address = child.text
                        elif col == 'IpPort':
                            ip_port = child.text
                        elif col == 'WorkstationName':
                            workstation_name = child.text
                    except KeyError:
                        pass
                else:
                    pass
            if event_id is None or time_created is None:
                continue
            if event_id in target_event_ids:
                ret.append(
                    (event_id, time_created, ip_address,
                     ip_port, workstation_name)
                )
        return ret

def main():

    parser = argparse.ArgumentParser(
        description="Process evtx file and get corresponding " +
                    "information of events with one or more event_ids."
    )
    parser.add_argument('evtx_filename', type=str)
    parser.add_argument('event_ids', type=int, nargs='+')
    args = parser.parse_args()
    print parse_evtx(args.evtx_filename, args.event_ids)


if __name__ == '__main__':

    main()
