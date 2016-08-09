__author__ = 'Arthur'
"""
This module is used to cluster the passengers into different group,
each of which is led by a driver.
"""

import datetime
import googlemaps
from datetime import datetime

import Member, APIkey



def psgr_cluster(dvr_list, psg_list):
    myname = "psgr_cluster"
    key = APIkey()
    gmap = googlemaps.Client(key=key)

    #set_member_coord(dvr_list, gmap)
    #set_member_coord(psg_list, gmap)

    now = datetime.datetime.now()
    for psg in psg_list:
        best_dr = None
        best_DandT = tuple(0, 0)
        for dr in dvr_list:
            tmp = gmap.directions(dr.get_address(), psg.get_address(), mode="driving", now)
            tmp_dis = tmp[0].get("legs")[0].get("distance").get("value")
            tmp_time = tmp[0].get("legs")[0].get("duration_in_traffic").get("value")

            if not best_dr:
                best_dr = dr
                best_DandT[0] = tmp_dis
                best_DandT[1] = tmp_time
            else:
                if tmp_dis < best_DandT[0] or tmp_time < best_DandT[1]:
                    best_dr = dr
                    best_DandT[0] = tmp_dis
                    best_DandT[1] = tmp_time

        dr.add_psg(psg);










def set_member_coord(member_list, gmap):
    for member in member_list:
        if not member.get_address():
            coord = gmap.geocode(member.get_address())
            coord = coord.get("geometry").get("bounds").get("northeast")
            member.set_coord(coord)
        else:
            message("Member " + member.get_name() + " address is missing")

    return


def message(msg, func_name="default"):
    print("Error - " + func_name +
          ": " + msg)



































if __name__ == '__main__':
    psgr_cluster()
