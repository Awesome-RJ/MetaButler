from MetaButler.modules.helper_funcs.extraction import extract_user
from MetaButler.modules.helper_funcs.decorators import metacmd
import requests, telegram, datetime, time

@metacmd(command="spbinfo")
def lookup(update, context):
    message = update.effective_message
    args = context.args
    user_id = extract_user(message, args)
    url = f"https://api.intellivoid.net/spamprotection/v1/lookup?query={user_id}"
    r = requests.get(url)
    a = r.json()
    response = a["success"]
    if response is True:
        date = a["results"]["last_updated"]
        stats = "**◢ Intellivoid• SpamProtection Info**:\\n"
        stats += f' • **Updated on**: `{datetime.datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S %p")}`\n'
        stats += (
            f" • **Chat Info**: [Link](t.me/SpamProtectionBot/?start=00_{user_id})\n"
        )

        if a["results"]["attributes"]["is_potential_spammer"] is True:
            stats += " • *User*: `USERxSPAM`\\n"
        elif a["results"]["attributes"]["is_operator"] is True:
            stats += " • *User*: `USERxOPERATOR`\\n"
        elif a["results"]["attributes"]["is_agent"] is True:
            stats += " • *User*: `USERxAGENT`\\n"
        elif a["results"]["attributes"]["is_whitelisted"] is True:
            stats += " • *User*: `USERxWHITELISTED`\\n"

        stats += f' • *Type*: `{a["results"]["entity_type"]}`\n'
        stats += (
            f' • *Language*: `{a["results"]["language_prediction"]["language"]}`\n'
        )
        stats += f' • *Language Probability*: `{a["results"]["language_prediction"]["probability"]}`\n'
        stats += "*Spam Prediction*:\\n"
        stats += f' • *Ham Prediction*: `{a["results"]["spam_prediction"]["ham_prediction"]}`\n'
        stats += f' • *Spam Prediction*: `{a["results"]["spam_prediction"]["spam_prediction"]}`\n'
        stats += f'*Blacklisted*: `{a["results"]["attributes"]["is_blacklisted"]}`\n'
        if a["results"]["attributes"]["is_blacklisted"] is True:
            stats += (
                f' • *Reason*: `{a["results"]["attributes"]["blacklist_reason"]}`\n'
            )
            stats += f' • *Flag*: `{a["results"]["attributes"]["blacklist_flag"]}`\n'
        stats += f'*PTID*:\n`{a["results"]["private_telegram_id"]}`\n'
        message.reply_text(stats, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        message.reply_text("`cannot reach SpamProtection API`")
        time.sleep(3)