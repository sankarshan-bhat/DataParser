from re import sub

# delimiter
columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Escape double quotes in a string
and surround all strings with double quotes
"""
def transformStr(st):
    # return NULL string for SQL as per spec.
    if st is None:
        return '"NULL"'

    escaped_str = sub(r'"', "", st)
    return '"{}"'.format(escaped_str)


"""
    Main class for Item
"""
class Item:
    # for printing items later
    item_lst = []

    def __init__(self, item_dict):
        # update with defaults, helps while printing
        self.itemid = '"NULL"'
        self.name = '"NULL"'
        self.currently = '"NULL"'
        self.buy_price = '"NULL"'
        self.first_bid ='"NULL"'
        self.number_of_bids = '"NULL"'
        self.started = '"NULL"'
        self.ends = '"NULL"'
        self.description = '"NULL"'
        self.sellerid = '"NULL"'
        self.bids = []

        try:
            self.itemid = item_dict["ItemID"]
        except KeyError:
            pass

        try:
            self.name = transformStr(item_dict["Name"])
        except KeyError:
            pass

        try:
            self.currently = transformDollar(item_dict["Currently"])
        except KeyError:
            pass

        try:
            self.buy_price = transformDollar(item_dict["Buy_Price"])
        except KeyError:
            pass

        try:
            self.first_bid = transformDollar(item_dict["First_Bid"])
        except KeyError:
            pass

        try:
            self.number_of_bids = item_dict["Number_of_Bids"]
        except KeyError:
            pass

        try:
            self.started = transformDttm(item_dict["Started"])
        except KeyError:
            pass

        try:
            self.ends = transformDttm(item_dict["Ends"])
        except KeyError:
            pass

        try:
            self.description = transformStr(item_dict["Description"])
        except KeyError:
            pass

        try:
            category_lst = item_dict["Category"]
            if category_lst is not None:
                for category_name in category_lst:
                    # a category may already exist
                    category = Category.get_or_create(category_name)

                    # update the many to many table
                    ItemCategory(self.itemid, category.categoryid)
        except KeyError:
            pass

        try:
            bid_lst = item_dict["Bids"]
            if bid_lst is not None:
                for bid in bid_lst:
                    bid_dict = bid["Bid"]
                    self.bids.append(Bid(bid_dict, self.itemid))
        except KeyError:
            pass

        try:
            seller_dict = item_dict["Seller"]

            try:
                seller_dict["Location"] = transformStr(item_dict["Location"])
            except KeyError:
                pass

            try:
                seller_dict["Country"] = transformStr(item_dict["Country"])
            except KeyError:
                pass

            seller = User.get_or_create(seller_dict, is_seller=True)
            self.sellerid = seller.userid
        except KeyError:
            pass

        # add to static item list
        Item.item_lst.append(self)

    def __str__(self):
        return columnSeparator.join(map(str, [
            self.itemid,
            self.name,
            self.currently,
            self.buy_price,
            self.first_bid,
            self.number_of_bids,
            self.started,
            self.ends,
            self.sellerid,
            self.description,
        ]))


class Bid:
    # useful for keeping bidid
    counter = 0

    # for printing bids later
    bid_lst = []

    def __init__(self, bid_dict, itemid):
        Bid.counter += 1

        self.bidid = Bid.counter
        self.itemid = itemid

        # assign defaults acc. to spec
        self.bidderid = '"NULL"'
        self.time = '"NULL"'
        self.amount = '"NULL"'

        try:
            self.time = transformDttm(bid_dict["Time"])
        except KeyError:
            pass

        try:
            self.amount = transformDollar(bid_dict["Amount"])
        except KeyError:
            pass

        try:
            bidder_dict = bid_dict["Bidder"]

            # a user may already exist
            bidder = User.get_or_create(bidder_dict, is_bidder=True)
            self.bidderid = bidder.userid
        except KeyError:
            pass

        Bid.bid_lst.append(self)

    def __str__(self):
        return columnSeparator.join(map(str, [
            self.bidid,
            self.bidderid,
            self.time,
            self.amount,
            self.itemid,

        ]))


class User:
    # static map for storing userid vs User to avoid duplicates
    user_map = {}
    counter = 0

    def __init__(self, userid):
        self.userid = userid

        # handle defaults
        self.is_seller = False
        self.is_bidder = False
        self.rating = '"NULL"'
        self.location = '"NULL"'
        self.country = '"NULL"'

    def update(self, user_dict, is_bidder,is_seller):
        # it's possible to receive attributes afterwards
        # so update them is possible
        try:
            self.rating = user_dict["Rating"]
        except KeyError:
            pass

        try:
            self.location = transformStr(user_dict["Location"])
        except KeyError:
            pass

        try:
            self.country = transformStr(user_dict["Country"])
        except KeyError:
            pass

        # if we know user is a seller, don't update again
        # since we may update it as False
        if not self.is_seller:
            self.is_seller = is_seller

        # if we know user is a bidder, don't update again
        # since we may update it as False
        if not self.is_bidder:
            self.is_bidder = is_bidder

    @classmethod
    def get_or_create(kls, user_dict, is_bidder=False, is_seller=False):
        userid = user_dict["UserID"]

        try:
            user = User.user_map[userid]
        except KeyError:
            user = kls(userid)

        # we may get newer attributes afterwards
        user.update(user_dict, is_bidder, is_seller)

        # update the dict with updated values
        User.user_map[userid] = user

        return user

    def __str__(self):
        return columnSeparator.join(map(str, [
            self.userid,
            self.rating,
            self.location,
            self.country,
            self.is_seller,
            self.is_bidder,
        ]))


class Category:
    # auto increment field for generating category id
    counter = 0

    # static map for storing category id vs Category to avoid duplicates
    category_map = {}

    def __init__(self, name):
        Category.counter += 1

        self.categoryid = Category.counter
        self.name = transformStr(name)

    @classmethod
    def get_or_create(kls, name):
        if name not in Category.category_map:
            Category.category_map[name] = kls(name)

        return Category.category_map[name]

    def __str__(self):
        return columnSeparator.join(map(str, [
            self.categoryid,
            self.name
        ]))


class ItemCategory:
    # for printing item-category relation later
    item_category_lst = set()

    def __init__(self, itemid, categoryid):
        self.itemid = itemid
        self.categoryid = categoryid

        self.item_category_lst.add(self)

    def __hash__(self):
        return hash((self.itemid, self.categoryid))

    def __eq__(self, other):
        if isinstance(other, ItemCategory):
            return self.itemid == other.itemid \
                and self.categoryid == other.categoryid
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return columnSeparator.join(map(str, [
            self.itemid,
            self.categoryid
        ]))

