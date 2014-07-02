# coding: utf-8

from pony.orm import Required
from ._base import db, SessionMixin, ModelMixin
import models as m
import config

config = config.rec()


class Bank(db.Entity, SessionMixin, ModelMixin):
    balance = Required(int, default=config.bank_init_coin)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Bank: %s>' % self.id

    @staticmethod
    def get_one():
        bank = Bank.get(id=1)
        if not bank:
            bank = Bank()
            bank.save()
        return bank

    def income(self, coin, role="topic-create", topic_id=None, reply_id=None,
               spender_id=None, incomer_id=None):
        self.balance += coin
        bill = m.Bill(coin=coin, balance=self.balance, role=role, category=1,
                      topic_id=topic_id, reply_id=reply_id,
                      spender_id=spender_id, incomer_id=incomer_id)
        bill.save()

    def spend(self, coin, role="signup", spender_id=None, incomer_id=None):
        self.balance -= coin
        bill = m.Bill(coin=coin, balance=self.balance, role=role, category=0,
                      spender_id=spender_id, incomer_id=incomer_id)
        bill.save()
