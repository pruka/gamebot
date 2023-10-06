from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
import random
from data import *
import time
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


bot = Client(
    "bulmaca_bot",
    api_id = 27924368,
    api_hash = "78dcc9a9d25d1386b508d37774b93f47",
    bot_token="5440371886:AAHfa9NE0EggD48BQy8XwdacWWJvllp6lFY"
)

@bot.on_message(filters.command("start"))
async def start(bot:Client, message:Message):
    chat_id = message.chat.id
    name = message.from_user.first_name
    text = f"Merhaba {name} bulmaca botuna hoş geldiniz!"
    await bot.send_message(chat_id, text)

kullanıcılar = {}

def tablo_oluştur(dictionary:dict):
    txt = ""
    liste = dictionary["terimler"]
    random.shuffle(liste)
    txt = dictionary["baslik"] + "\n"
    for i in enumerate(liste, 1):
        txt += f"{i[0]}. "+len(i[1])*"_ "+"\n"
    return txt, liste

dicts = [biyoloji, tarih, cografya, tarkan]
@bot.on_message(filters.command("oyun"))
async def oyun(bot:Client, message:Message):
    chat_id = message.chat.id
    if chat_id in list(kullanıcılar.keys()):
        kullanıcılar.pop(chat_id, None)
    secilendicts = random.choices(dicts)
    tablo,liste = tablo_oluştur(secilendicts[0])
    msg = await bot.send_message(chat_id, tablo, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="İpucu 🔏", callback_data="ipucu")]]))
    t0 = time.time()
    kullanıcılar.update({chat_id:{"msg_id":msg.id, "liste":liste, "tablo":tablo, "say":0, "zaman":int(t0)}})


@bot.on_message(filters.text)
async def sorgulama(bot:Client, message:Message):
    text = (message.text).lower()
    chat_id = message.chat.id
    id = message.from_user.id
    isim = message.from_user.first_name
    bilinenkelimelistesi = list()
    puanisimlist = list()
    try:
        tablokelimeliste = list(kullanıcılar.get(chat_id, "")["liste"])
    except IndexError:
        return
    except KeyError:
        return
    except TypeError:
        return
    if text in tablokelimeliste:
        tablokelime = str(kullanıcılar.get(chat_id, "")["tablo"])
        tablokelimelist = tablokelime.split("\n")
        kelimesırası = kullanıcılar[chat_id]["liste"].index(text)
        puan = int()
        try:
            bilinenkelimelistesi = kullanıcılar[chat_id]["bilinenkelimeler"]
            puanisimlist = kullanıcılar[chat_id]["puanisimlist"]
        except:
            pass            
        if text in bilinenkelimelistesi:
            return
        tablokelime = tablokelime.replace(tablokelimelist[kelimesırası+1], f"{kelimesırası+1}. {text}")

        if isim in tablokelime:
            index = tablokelime.index(isim)
            puan = int(tablokelime[index+len(isim)+3:].split("\n", 1)[0])
            puan += len(text)
            tablokelime = tablokelime.replace(f"{isim} ↣ {puan-len(text)}", f"{isim} ↣ {puan}")
        else:
            if "↣" in tablokelime:
                tablokelime += f"{isim} ↣ {len(text)}\n"
            else:
                tablokelime += f"\n💠 OYUNCULAR 💠\n{isim} ↣ {len(text)}\n"
            puan = len(text)
        await bot.send_message(chat_id, tablokelime, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="İpucu 🔏", callback_data="ipucu")]]))
        bilinenkelimelistesi.append(text)
        
        if idVarmi(puanisimlist, id) == None:
            puanisimlist.append({"isim":isim, "puan":puan, "id":id})
        else:
            indexno = idVarmi(puanisimlist, id)
            puanisimlist[indexno] = {"isim":isim, "puan":puan, "id":id}
        kullanıcılar[chat_id].update({"liste":tablokelimeliste, "tablo":tablokelime, "bilinenkelimeler":bilinenkelimelistesi, "puanisimlist":puanisimlist})
        say = kullanıcılar[chat_id]["say"]
        say += 1
        kullanıcılar[chat_id]["say"] = say
        puanartır(id=id, nekadar=len(text), isim=isim)
        
    else:
        for i in text.split(" "):
            if i in tablokelimeliste:
                tablokelime = str(kullanıcılar.get(chat_id, "")["tablo"])
                tablokelimelist = tablokelime.split("\n")
                kelimesırası = kullanıcılar[chat_id]["liste"].index(i)
                puan = int()
                try:
                    bilinenkelimelistesi = kullanıcılar[chat_id]["bilinenkelimeler"]
                    puanisimlist = kullanıcılar[chat_id]["puanisimlist"]
                except:
                    pass
                if i in bilinenkelimelistesi:
                    return
                tablokelime = tablokelime.replace(tablokelimelist[kelimesırası+1], f"{kelimesırası+1}. {i}")

                if isim in tablokelime:
                    index = tablokelime.index(isim)
                    puan = int(tablokelime[index+len(isim)+3:].split("\n", 1)[0])
                    puan += len(i)
                    tablokelime = tablokelime.replace(f"{isim} ↣ {puan-len(i)}", f"{isim} ↣ {puan}")
                else:
                    if "↣" in tablokelime:
                        tablokelime += f"{isim} ↣ {len(i)}\n"
                    else:
                        tablokelime += f"\n💠 OYUNCULAR 💠\n{isim} ↣ {len(i)}\n"
                    puan = len(i)
                await bot.send_message(chat_id, tablokelime, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="İpucu 🔏", callback_data="ipucu")]]))
                bilinenkelimelistesi.append(i)
                if idVarmi(puanisimlist, id) == None:
                    puanisimlist.append({"isim":isim, "puan":puan, "id":id})
                else:
                    indexno = idVarmi(puanisimlist, id)
                    puanisimlist[indexno] = {"isim":isim, "puan":puan, "id":id}
                kullanıcılar[chat_id].update({"liste":tablokelimeliste, "tablo":tablokelime, "bilinenkelimeler":bilinenkelimelistesi, "puanisimlist":puanisimlist})
                say = kullanıcılar[chat_id]["say"]
                say += 1
                kullanıcılar[chat_id]["say"] = say
                puanartır(id=id, nekadar=len(i), isim=isim)
    if kullanıcılar[chat_id]["say"] == len(kullanıcılar.get(chat_id, None).get("liste")):
        kazananisim = list(siraci(puanisimlist)[0].values())[0]
        kazananpuan = list(dict(siraci(puanisimlist)[0]).values())[1]
        await bot.send_message(chat_id, f"Tebrikler başarıyla bitirdiniz! 🌟\nKazanan : {kazananisim} ↦ {kazananpuan} 🏅", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Tekrar Oyna 🔫", callback_data="/oyun")]]))
        kullanıcılar.pop(chat_id, None)


def idVarmi(liste:list, id):
    indexsayisi = None
    for i in liste:
        deger = list(i.values())[2]
        if deger == id:
            indexsayisi = liste.index(i)
    return indexsayisi

def siraci(d:list):
    def get_puan(element):
        return element["puan"]
    d.sort(key=get_puan, reverse=True)
    return d

async def zamansorgucusu():
    await bot.start()
    while True:
        t0 = time.time()
        for i in list(kullanıcılar.keys()):
            if int(t0) - kullanıcılar[i]["zaman"] == 90:
                kullanıcılar.pop(i, None)
                await bot.send_message(i, "Size ayrılan sürenin sonuna geldik :(\n", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Tekrar Oyna 🔫", callback_data="/oyun")]]))
        await asyncio.sleep(0.7)


@bot.on_callback_query()
async def butonlar(bot:Client, CallbackQuery:CallbackQuery):
    data = CallbackQuery.data
    chat_id = CallbackQuery.message.chat.id
    callback_id = CallbackQuery.id
    if data == "/oyun":
        await oyun(bot=bot, message=CallbackQuery.message)

    if data == "ipucu":
        try:
            liste = kullanıcılar[chat_id]["liste"]
            tablo = kullanıcılar[chat_id]["tablo"]
            boslukliste = tablo.split("\n")
            baslik = boslukliste.pop(0)
            say = 0
            for i in liste:
                if boslukliste[say][3] == "_":
                    harf = i[0]
                    boslukliste[say] = boslukliste[say].replace("_", harf, 1)
                elif boslukliste[say][3] != "_" and boslukliste[say][-2] == "_":
                    harf = i[-1]
                    once = boslukliste[say][:-2]
                    sonra = boslukliste[say][-1:] 
                    boslukliste[say] = once+harf+sonra
                elif boslukliste[say][3] != "_" and boslukliste[say][-2] != "_" and boslukliste[say][5] == "_":
                    harf = i[1]
                    boslukliste[say] = boslukliste[say].replace("_", harf, 1)
                elif boslukliste[say][3] != "_" and boslukliste[say][-2] != "_" and boslukliste[say][5] != "_":
                    harf = i[-2]
                    once = boslukliste[say][:-4]
                    sonra = boslukliste[say][-3:] 
                    boslukliste[say] = once+harf+sonra
                elif boslukliste[say][3] != "_" and boslukliste[say][-2] != "_" and boslukliste[say][5] != "_" and boslukliste[say][7] == "_":
                    print("ben")
                    harf = i[2]
                    boslukliste[say] = boslukliste[say].replace("_", harf, 1)
                boslukliste[say][7]
                say += 1
            newtable = "\n".join(boslukliste)
            gonderilecek = f"{baslik}\n{newtable}"
            kullanıcılar[chat_id]["tablo"] = gonderilecek
            await CallbackQuery.edit_message_text(f"{baslik}\n{newtable}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="İpucu 🔏", callback_data="ipucu")]]))
        except Exception as e:
            print(e)
            if e.args[0] == chat_id:
                await bot.answer_callback_query(callback_id,  text="Aktif bir oyun bulunmuyor!", show_alert=True)
            else:
                await bot.answer_callback_query(callback_id,  text="İpucu hakkı bitti!", show_alert=True)

def puanartır(id, nekadar, isim):
    with open("puanlar.json", "r") as f:
        data = json.load(f)
    kisi = data["users"].get(str(id), "kisiyok")
    if kisi == "kisiyok":
        data["users"].update({id:{"puan":nekadar, "isim":isim}})
        with open("puanlar.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        puan = nekadar + data["users"].get(str(id), None).get("puan", 0)
        data["users"][str(id)]["puan"] = puan
        with open("puanlar.json", "w") as f:
            json.dump(data, f, indent=4)

@bot.on_message(filters.regex("msj"))
async def msj(bot, message):
    await message.reply(message)



print("bulmaca bot running")
bot.run(zamansorgucusu())