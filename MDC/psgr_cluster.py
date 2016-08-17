__author__ = 'Arthur'
"""
This module is used to cluster the passengers into different group,
each of which is led by a driver.
"""

import googlemaps
from datetime import datetime

from APIkey import APIkey
import data_input
import constants



def psgr_cluster(dvr_list, psg_list, car_capacity):
    myname = "psgr_cluster"
    key = APIkey()
    gmap = googlemaps.Client(key=key.get_key())

    if len(dvr_list) * car_capacity < len(psg_list):
        message("Error: Not enough driver, Failed to do optimization.")
        return None

    for psg in psg_list:
        restrict_area(psg)

    for dr in dvr_list:
        restrict_area(dr)

    for psg in psg_list:
        best_dr = None
        best_DandT = (0,0)
        for dr in dvr_list:
            if dr.get_psg_number() == car_capacity:
                continue

            tmp = gmap.directions(dr.get_address(), psg.get_address(), mode="driving",
                                  departure_time=datetime.now(), avoid="tolls", units="metric")
            if len(tmp) == 0:
                message("Distance between " + dr.get_address() + " and " + psg.get_address() + " is not calculable")
                return None
            tmp_dis = tmp[0].get("legs")[0].get("distance").get("value")
            tmp_time = tmp[0].get("legs")[0].get("duration_in_traffic").get("value")

            if not best_dr:
                best_dr = dr
                best_DandT = (tmp_dis, tmp_time)
            else:
                if tmp_dis < best_DandT[0] or tmp_time < best_DandT[1]:
                    best_dr = dr
                    best_DandT = (tmp_dis, tmp_time)

        best_dr.add_psg(psg);


def set_member_coord(member_list, gmap):
    for member in member_list:
        if not member.get_address():
            coord = gmap.geocode(member.get_address())
            coord = coord.get("geometry").get("bounds").get("northeast")
            member.set_coord(coord)
        else:
            message("Member " + member.get_name() + " address is missing")

    return


def restrict_area(member, region=constants.REGION, country=constants.COUNTRY):
    import re
    reg_match = re.compile("[a-zA-Z]")

    no_region = False
    no_country = False

    origin_addr = member.get_address().lower()
    region_index = origin_addr.rfind(region[1].lower())
    region_str_len = len(region[1])
    reg_match.match(origin_addr[region_index - 1])
    if region_index > 0 and not reg_match.match(origin_addr[region_index - 1]):
        if region_index + region_str_len == len(origin_addr):
            member.set_address(origin_addr[:region_index] + region[0])
        elif not reg_match.match(origin_addr[region_index + region_str_len]):
            member.set_address(origin_addr[:region_index] + region[0] + origin_addr[region_index + region_str_len:])
    else:
        no_region = True

    origin_addr = member.get_address().lower()
    ctr_index = origin_addr.rfind(country[1].lower())
    ctr_str_len = len(country[1])
    if ctr_index > 0 and not reg_match.match(origin_addr[ctr_index - 1]):
        if ctr_index + ctr_str_len == len(origin_addr):
            member.set_address(origin_addr[:ctr_index]+ country[0])
        elif not reg_match.match(origin_addr[ctr_index + ctr_str_len]):
            member.set_address(origin_addr[:ctr_index]+ country[0] + origin_addr[ctr_index + ctr_str_len])
    else:
        no_country = True

    if no_region:
        member.set_address(origin_addr + ", " + region[0])
    if no_country:
        member.set_address(member.get_address() + ", " + country[0])





def message(msg, func_name="default"):
    print("Error - " + func_name +
          ": " + msg)


if __name__ == '__main__':
    [d_list, p_list] = data_input.read_from_csv("test2.csv")
    psgr_cluster(d_list, p_list, 4)

    print("End")
