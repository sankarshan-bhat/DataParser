 select count(*) from (select distinct(categoryid) from itemscategoryrel ir inner join bids b on ir.itemid = b.itemid where b.amount >100 );