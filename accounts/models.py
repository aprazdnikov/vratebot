from django.db import models


# Create your models here.
class Account(models.Model):

    user_id = models.IntegerField(null=False, editable=False)
    user_name = models.CharField(max_length=255)
    btc_balance = models.IntegerField(null=False, blank=False)
    eth_balance = models.IntegerField(null=False, blank=False)

    def __unicode__(self):
        return f"Пользователь {self.user_name}\n" \
               f"Баланс: BTC - {self.btc_balance} | ETH - {self.eth_balance}"

    def __str__(self):
        return f"Пользователь {self.user_name}\n" \
               f"Баланс: BTC - {self.btc_balance} | ETH - {self.eth_balance}"

    def to_json(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'btc': self.btc_balance,
            'eth': self.eth_balance
        }
