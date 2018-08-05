# encoding: utf-8
from hashids import Hashids


def get_hashid(uid):
    hash_id = Hashids(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123567890', salt='1766',min_length=6)
    hashid = hash_id.encode(uid)
    return hashid
