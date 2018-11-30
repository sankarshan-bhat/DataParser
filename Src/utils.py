import models

def write_dat_files():
    # write dat file for categories
    with open('auctionCategory.dat', 'w') as fcategory:
        for category in models.Category.category_map.itervalues():
            fcategory.write(category.__str__() + '\n')

    # write dat file for users
    with open('auctionUser.dat', 'w') as fuser:
        for user in models.User.user_map.itervalues():
            fuser.write(user.__str__() + '\n')

    # write dat file for bids
    with open('auctionBid.dat', 'w') as fbid:
        for bid in models.Bid.bid_lst:
            fbid.write(bid.__str__() + '\n')

    # write dat file for items
    with open('auctionItem.dat', 'w') as fitem:
        for item in models.Item.item_lst:
            fitem.write(item.__str__() + '\n')

    # write data file item_category
    with open('auctionItemCategory.dat', 'w') as fitemcategory:
        for itemcategory in models.ItemCategory.item_category_lst:
            fitemcategory.write(itemcategory.__str__() + '\n')
