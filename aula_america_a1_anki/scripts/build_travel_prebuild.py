#!/usr/bin/env python3
import csv
import hashlib
import json
import os
import re
import sqlite3
import time
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "anki_travel_pack"
BASELINE = ROOT / "prebuilds" / "v047" / "anki_v047_nvh_u6_prebuild.tsv"

FIELDS = ["deck", "note_type", "front", "back", "extra", "tags"]


def norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def load_baseline():
    seen_front = set()
    seen_back = set()
    if not BASELINE.exists():
        return seen_front, seen_back
    with BASELINE.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            seen_front.add(norm(row["front"]))
            seen_back.add(norm(row["back"]))
    return seen_front, seen_back


class Builder:
    def __init__(self, version, name, deck, scope, review=False):
        self.version = version
        self.name = name
        self.deck = deck
        self.scope = scope
        self.review = review
        self.rows = []
        self.local_fronts = set()
        self.local_backs = set()
        self.skipped = []

    def add(self, front, back, extra="", tags=""):
        front = front.strip()
        back = back.strip()
        extra = extra.strip()
        full_tags = f"{tags} {self.version} {self.name}".strip()
        nf = norm(front)
        nb = norm(back)
        if nf in BASE_FRONTS or nb in BASE_BACKS or nf in self.local_fronts or nb in self.local_backs:
            self.skipped.append({"front": front, "back": back, "reason": "duplicate_front_or_back"})
            return
        self.local_fronts.add(nf)
        self.local_backs.add(nb)
        self.rows.append({
            "deck": self.deck,
            "note_type": "Basic",
            "front": front,
            "back": back,
            "extra": extra,
            "tags": tag_clean(full_tags),
        })


def tag_clean(tags):
    out = []
    for tag in tags.split():
        tag = tag.strip().lower()
        tag = re.sub(r"[^a-z0-9_]+", "_", tag)
        tag = re.sub(r"_+", "_", tag).strip("_")
        if tag:
            out.append(tag)
    return " ".join(dict.fromkeys(out))


def add_vocab(b, items, block, source="nvh_core", extra_default="名词建议连冠词一起记。"):
    for zh, es, extra in items:
        b.add(f"{zh}", es, extra or extra_default, f"{source} {block} vocab lexico")


def add_pairs(b, items, block, source="nvh_core", kind="phrase"):
    for zh, es, extra in items:
        b.add(zh, es, extra, f"{source} {block} {kind}")


def add_contrast(b, prompt, answer, extra, block, source="error_review"):
    b.add(prompt, answer, extra, f"{source} {block} contrast error_review")


BASE_FRONTS, BASE_BACKS = load_baseline()


def build_u7():
    b = Builder(
        "anki_v048",
        "anki_v048_nvh_u7_prebuild",
        "Spanish::Nos vemos hoy::U7 El placer de viajar",
        "NVH U7 prebuild: lodging, recommendations, agreement, travel experiences, complaints",
    )
    add_vocab(b, [
        ("房间；连冠词", "la habitación", ""),
        ("双人间；连冠词", "la habitación doble", ""),
        ("单人间；连冠词", "la habitación individual", ""),
        ("外侧/临街房间；连冠词", "la habitación exterior", ""),
        ("内侧/不临街房间；连冠词", "la habitación interior", ""),
        ("安静的房间；连冠词", "la habitación tranquila", ""),
        ("吵的房间；连冠词", "la habitación ruidosa", ""),
        ("完整浴室；连冠词", "el baño completo", ""),
        ("淋浴；连冠词", "la ducha", ""),
        ("浴缸；连冠词", "la bañera", ""),
        ("阳台；连冠词", "el balcón", ""),
        ("海景；连冠词", "las vistas al mar", "通常用复数 vistas。"),
        ("早餐；连冠词", "el desayuno", ""),
        ("自助早餐；连冠词", "el desayuno bufé", ""),
        ("早餐已包含", "desayuno incluido", ""),
        ("停车场；连冠词", "el aparcamiento", "西班牙常见；拉美也常说 el estacionamiento。"),
        ("停车场；拉美常见；连冠词", "el estacionamiento", "Aula/LatAm 对照补充。"),
        ("游泳池；连冠词", "la piscina", ""),
        ("健身房；连冠词", "el gimnasio", ""),
        ("桑拿；连冠词", "la sauna", ""),
        ("空调；连冠词", "el aire acondicionado", ""),
        ("网络连接；连冠词", "la conexión a internet", ""),
        ("价格；连冠词", "el precio", ""),
        ("预订；连冠词", "la reserva", ""),
        ("服务；复数；连冠词", "los servicios", ""),
        ("乡村民宿/乡村房；连冠词", "la casa rural", "教材语境；拉美旅行时也可根据国家说 cabaña, finca 等。"),
    ], "u7_block_02")

    add_pairs(b, [
        ("我想预订一个房间。", "Quería reservar una habitación.", "礼貌说法；酒店电话/前台都很自然。"),
        ("我想预订一间双人房，住两晚。", "Quería reservar una habitación doble para dos noches.", ""),
        ("一间带完整浴室的单人房，谢谢。", "Una habitación individual con baño completo, por favor.", ""),
        ("房价含早餐吗？", "¿El precio incluye el desayuno?", ""),
        ("早餐包含在内吗？", "¿El desayuno está incluido?", ""),
        ("房间有空调吗？", "¿La habitación tiene aire acondicionado?", ""),
        ("房间有无线网吗？", "¿La habitación tiene wifi?", ""),
        ("有停车场吗？", "¿Tienen estacionamiento?", "LatAm travel upgrade；比 aparcamiento 在美洲更常见。"),
        ("我想要一间安静一点的房间。", "Quería una habitación más tranquila.", ""),
        ("我想要一间不临街的房间。", "Quería una habitación interior.", ""),
        ("有海景房吗？", "¿Tienen habitaciones con vistas al mar?", ""),
        ("我要住三晚。", "Me quedo tres noches.", "实用入住表达；比只会 para tres noches 更能说完整句。"),
        ("我今天晚上到。", "Llego esta noche.", ""),
        ("我大概晚上九点到。", "Llego sobre las nueve de la noche.", ""),
        ("可以刷卡吗？", "¿Puedo pagar con tarjeta?", "若 v047/U5 已有 ¿Aceptan tarjeta?，这里用不同前台表达。"),
        ("我可以寄存行李吗？", "¿Puedo dejar mi equipaje?", "酒店高频补充。"),
        ("退房时间是几点？", "¿A qué hora es el check-out?", "拉美/旅游场景常混用 check-out。"),
        ("早餐几点开始？", "¿A qué hora empieza el desayuno?", ""),
        ("到机场的下一班公交几点发车？", "¿A qué hora sale el próximo autobús al aeropuerto?", ""),
        ("酒店离市中心近吗？", "¿El hotel está cerca del centro?", "和 U6 hay/estar 接轨。"),
    ], "u7_block_02")

    add_pairs(b, [
        ("在马略卡可以徒步。", "En Mallorca se puede hacer senderismo.", ""),
        ("在这里可以去海边。", "Aquí se puede ir a la playa.", ""),
        ("在这里可以晒太阳。", "Aquí se puede tomar el sol.", ""),
        ("在这里可以尝当地菜。", "Aquí se puede probar la comida local.", "LatAm 更通用：comida local。"),
        ("这座城市适合休息。", "Esta ciudad es ideal para descansar.", ""),
        ("这个地方适合拍照。", "Este lugar es perfecto para hacer fotos.", ""),
        ("我想参观历史中心。", "Quiero visitar el centro histórico.", ""),
        ("我们可以做一日游。", "Podemos hacer una excursión de un día.", ""),
        ("附近有什么好玩的？", "¿Qué se puede hacer por aquí?", "LatAm travel upgrade。"),
        ("您推荐什么地方？", "¿Qué lugar me recomienda?", "usted 场景，旅行中更安全。"),
        ("您推荐哪个海滩？", "¿Qué playa me recomienda?", ""),
        ("有什么典型的菜可以尝？", "¿Qué plato típico puedo probar?", ""),
    ], "u7_block_01")

    add_vocab(b, [
        ("假期；复数；连冠词", "las vacaciones", ""),
        ("旅行；连冠词", "el viaje", ""),
        ("有组织的旅行/跟团游；连冠词", "el viaje organizado", ""),
        ("路线/行程；连冠词", "el itinerario", ""),
        ("行李；连冠词", "el equipaje", ""),
        ("票；旅行票；连冠词", "los billetes", "西班牙常见；美洲可用 boletos。"),
        ("票；拉美常见；连冠词", "los boletos", "Aula/LatAm 对照补充。"),
        ("导游书/旅行指南；连冠词", "la guía", ""),
        ("领事馆；连冠词", "el consulado", ""),
        ("钱；连冠词", "el dinero", ""),
        ("餐桌预订；连冠词", "la reserva de mesa", ""),
    ], "u7_block_05")

    add_pairs(b, [
        ("你去过拉美吗？", "¿Has estado en Latinoamérica?", ""),
        ("你在旅行中说过西语吗？", "¿Has hablado español en un viaje?", ""),
        ("你尝过墨西哥菜吗？", "¿Has probado comida mexicana?", ""),
        ("你住过五星级酒店吗？", "¿Has dormido alguna vez en un hotel de cinco estrellas?", ""),
        ("我今年去了墨西哥。", "Este año he ido a México.", ""),
        ("我这周到了厄瓜多尔。", "Esta semana he llegado a Ecuador.", ""),
        ("我已经买票了。", "Ya he comprado los boletos.", "LatAm 对照：boletos。"),
        ("我还没有订酒店。", "Todavía no he reservado el hotel.", ""),
        ("我从来没去过古巴。", "Nunca he estado en Cuba.", ""),
        ("我参观了几个博物馆。", "He visitado varios museos.", ""),
        ("我看到了很美的地方。", "He visto lugares muy bonitos.", ""),
        ("我做了一次山里的一日游。", "He hecho una excursión a la montaña.", ""),
        ("我吃了很多新东西。", "He comido muchas cosas nuevas.", ""),
        ("我已经做好行李了。", "Ya he hecho el equipaje.", ""),
        ("你换钱了吗？", "¿Has cambiado dinero?", ""),
        ("你租车了吗？", "¿Has alquilado un coche?", "拉美也常说 rentar un carro；此处保留教材词。"),
        ("你下载旅行指南了吗？", "¿Te has bajado una guía de viaje?", "识别即可；也可说 descargado。"),
        ("更通用地说“下载旅行指南”", "descargar una guía de viaje", "LatAm/现代口语更透明。"),
    ], "u7_block_05")

    add_pairs(b, [
        ("我喜欢山。", "Me gusta la montaña.", ""),
        ("我爸喜欢海。", "A mi padre le gusta el mar.", ""),
        ("我妈喜欢自然。", "A mi madre le gusta la naturaleza.", ""),
        ("他们喜欢安静的酒店。", "Les gustan los hoteles tranquilos.", ""),
        ("我对文化感兴趣。", "Me interesa la cultura.", ""),
        ("我对博物馆感兴趣。", "Me interesan los museos.", ""),
        ("噪音让我烦。", "Me molesta el ruido.", ""),
        ("贵酒店让我烦。", "Me molestan los hoteles caros.", ""),
        ("旅行时你喜欢走路吗？", "¿Te gusta caminar cuando viajas?", ""),
        ("旅行时你喜欢即兴安排吗？", "¿Te gusta improvisar cuando viajas?", ""),
        ("我也喜欢。", "A mí también.", "回应 Me gusta... / Me encanta...。"),
        ("我也不喜欢。", "A mí tampoco.", "回应 No me gusta...。"),
        ("我喜欢。", "Pues a mí sí.", "回应别人 No me gusta... 时表达相反。"),
        ("我不喜欢。", "Pues a mí no.", "回应别人 Me gusta... 时表达相反。"),
    ], "u7_block_03 u7_block_04")

    add_pairs(b, [
        ("不好意思，我有个小问题。", "Perdone, tengo un pequeño problema.", ""),
        ("不好意思，我没有点汤，而是点了沙拉。", "Perdone, no he pedido sopa, sino ensalada.", ""),
        ("不好意思，我要的是有气水，不是无气水。", "Perdone, he pedido agua con gas, no agua sin gas.", ""),
        ("我预订的是有浴缸的房间。", "He reservado una habitación con bañera.", ""),
        ("但是这里只是淋浴。", "Pero solo tengo ducha.", ""),
        ("空调坏了。", "El aire acondicionado no funciona.", ""),
        ("无线网不好用。", "El wifi no funciona bien.", ""),
        ("房间有点脏。", "La habitación está un poco sucia.", ""),
        ("我们马上给您换一间。", "Enseguida le damos otra habitación.", ""),
        ("抱歉，这是我们的错误。", "Lo siento. Ha sido un error.", ""),
        ("抱歉给您带来不便。", "Perdone las molestias.", ""),
        ("没关系。", "No pasa nada.", ""),
        ("好的，谢谢。", "Está bien, gracias.", ""),
    ], "u7_block_06")

    for verb, part in [
        ("visitar", "visitado"), ("comer", "comido"), ("vivir", "vivido"),
        ("ir", "ido"), ("ser", "sido"), ("ver", "visto"), ("hacer", "hecho"),
        ("poner", "puesto"), ("decir", "dicho"), ("abrir", "abierto"),
        ("escribir", "escrito"), ("volver", "vuelto"),
    ]:
        b.add(f"`{verb}` 的现在完成时分词", part, "只先服务旅行经历表达，不展开完整过去时系统。", "nvh_core u7_block_05 grammar participio")

    for zh, es in [
        ("我做", "hago"), ("我放/我穿", "pongo"), ("我出去", "salgo"),
        ("我带来", "traigo"), ("我说", "digo"), ("我来", "vengo"),
    ]:
        b.add(f"{zh}；-go 第一人称", es, "先识别高频 yo 形式。", "nvh_core u7_block_04 grammar verb_g")

    add_contrast(b, "“我也不喜欢城市假期”：A mí también 还是 A mí tampoco？", "A mí tampoco.", "前一句是否定：No me gustan las vacaciones en las ciudades.", "u7_block_04")
    add_contrast(b, "“房价包含早餐吗？”不要说 ¿El precio es desayuno?，自然说法是？", "¿El precio incluye el desayuno?", "include = incluir；酒店场景常用。", "u7_block_02")
    add_contrast(b, "“我没有点 A，而是 B”：核心结构", "No he pedido A, sino B.", "sino 用来纠正前面的否定内容。", "u7_block_06")
    add_contrast(b, "“我已经买票了”：ya 放在哪里？", "Ya he comprado los boletos.", "ya 通常放在完成时结构前面。", "u7_block_05")
    add_contrast(b, "“我还没订酒店”：todavía no + 完成时", "Todavía no he reservado el hotel.", "no 放在 haber 前面。", "u7_block_05")
    return b


def build_u8():
    b = Builder(
        "anki_v049",
        "anki_v049_nvh_u8_mirador_review",
        "Spanish::Nos vemos hoy::U8 Mirador review",
        "NVH U8 Mirador review: U5-U7 integration, no heavy new grammar",
        review=True,
    )
    add_pairs(b, [
        ("市场里，店员常说：还要别的吗？", "¿Algo más?", ""),
        ("市场里，顾客常说：给我半公斤。", "Deme medio kilo.", ""),
        ("市场里，顾客常说：多少钱？", "¿Cuánto es?", ""),
        ("市场里，顾客常说：就这些。", "Eso es todo.", ""),
        ("市场里，店员常说：一共十二欧。", "En total son doce euros.", ""),
        ("市场里，店员常说：不好意思，今天没有。", "Lo siento, hoy no tengo.", ""),
        ("市场/小店结束时：下次见！", "¡Hasta la próxima!", ""),
    ], "u8_review_02", "nvh_core", "review_phrase")

    add_pairs(b, [
        ("复习整合：酒店房间是内侧而且很安静。", "La habitación es interior y muy tranquila.", ""),
        ("复习整合：在车站直接买。", "En la estación directamente.", ""),
        ("复习整合：每天上午十一点都有。", "Sí, todos los días a las once.", ""),
        ("复习整合：七月没有，只有八月。", "En julio no, solo en agosto.", ""),
        ("复习整合：在下一站下。", "En la próxima parada.", ""),
        ("复习整合：十五到三十欧之间。", "Entre quince y treinta euros.", ""),
    ], "u8_review_03", "nvh_core", "review_phrase")

    add_pairs(b, [
        ("描述城市：它在哪里？", "¿Dónde está?", ""),
        ("描述城市：那里有什么？", "¿Qué hay?", ""),
        ("描述城市：你喜欢什么？", "¿Qué te gusta?", ""),
        ("我喜欢步行逛市中心。", "Me gusta pasear por el centro a pie.", ""),
        ("我喜欢去博物馆。", "Me gusta ir a museos.", ""),
        ("我喜欢尝当地菜。", "Me gusta probar la comida local.", ""),
        ("我们俩都喜欢拍照。", "A los dos nos gusta hacer fotos.", "U8 输出卡，回收 gustar。"),
        ("我喜欢购物，但我朋友不喜欢。", "A mí me gusta ir de compras, pero a mi amigo no.", ""),
    ], "u8_review_04", "nvh_core", "review_phrase")

    add_pairs(b, [
        ("听机场广播找航班口：你主要在听什么？", "filtrar información", "听力策略识别卡：筛选特定信息。"),
        ("听一个旅游播客了解大意：你主要在听什么？", "captar el sentido", "听力策略识别卡：抓大意。"),
        ("听别人问几点：你需要什么程度？", "entender todo exactamente", "短句功能强，适合精确理解。"),
        ("别人解释从车站到市中心怎么走：你主要先听什么？", "filtrar información", "抓地点、方向、交通方式。"),
    ], "u8_review_05", "nvh_core", "strategy")

    add_pairs(b, [
        ("酒吧文化：我们分账。", "Dividimos la cuenta.", "拉美/旅行实用表达。"),
        ("这顿我请。", "Invito yo.", "自然口语；不是 pedir。"),
        ("小费包含了吗？", "¿La propina está incluida?", "Aula América 文化补充。"),
        ("我们坐吧台可以吗？", "¿Podemos sentarnos en la barra?", ""),
        ("可以和别人拼桌吗？", "¿Podemos compartir una mesa?", ""),
        ("早餐不总是包含在酒店价格里。", "El desayuno no siempre está incluido en el precio del hotel.", ""),
    ], "u8_review_01", "aula_america_alignment latam_travel_upgrade", "culture_phrase")

    add_contrast(b, "改错：Por fin soy en Bolivia.", "Por fin estoy en Bolivia.", "位置/状态用 estar。", "u8_review_06")
    add_contrast(b, "改错：una familla muy sympática", "una familia muy simpática", "拼写：familia, simpática。", "u8_review_06")
    add_contrast(b, "改错：trabaja en una officina a Cochabamba", "trabaja en una oficina en Cochabamba", "城市里用 en；oficina 一个 f。", "u8_review_06")
    add_contrast(b, "改错：Yo trabaja en una escuela al centro.", "Yo trabajo en una escuela en el centro.", "yo trabajo；在市中心 en el centro。", "u8_review_06")
    add_contrast(b, "改错：Me pagan mil cincuentos pesos.", "Me pagan mil quinientos pesos.", "1500 = mil quinientos。", "u8_review_06")
    add_contrast(b, "改错：Todavía he no ido a La Paz.", "Todavía no he ido a La Paz.", "no 放在 he 前面。", "u8_review_06")
    add_contrast(b, "改错：Quiero la visitar.", "Quiero visitarla.", "代词接在 infinitivo 后面：visitarla。", "u8_review_06")
    add_contrast(b, "改错：Vas en Allemania con coche?", "¿Vas a Alemania en coche?", "去某地用 a；交通方式 en coche。", "u8_review_06")

    for front, back, extra in [
        ("U8 综合输出：我在玻利维亚，住在一个友好的家庭家里。", "Estoy en Bolivia y vivo con una familia muy simpática.", ""),
        ("U8 综合输出：我想参观首都和博物馆。", "Quiero visitar la capital y ver los museos.", ""),
        ("U8 综合输出：我还没去 La Paz，但是十月去。", "Todavía no he ido a La Paz, pero voy en octubre.", ""),
        ("U8 综合输出：这个城市有很多餐厅，市中心很有意思。", "Hay muchos restaurantes y el centro es muy interesante.", ""),
        ("U8 综合输出：我喜欢步行，但是如果很远，我坐出租车。", "Me gusta caminar, pero si está muy lejos, voy en taxi.", ""),
    ]:
        b.add(front, back, extra, "review_bridge u8_review_06 output")

    add_pairs(b, [
        ("U8 餐厅整合：我想要一杯水，不加冰。", "Quería un vaso de agua sin hielo.", "回收 U5 点餐 + U7 礼貌请求。"),
        ("U8 餐厅整合：我没有点这个。", "No he pedido esto.", "U7 投诉 + U9 esto 预热。"),
        ("U8 餐厅整合：账单可以分开吗？", "¿Podemos pagar por separado?", "LatAm 旅行实用。"),
        ("U8 餐厅整合：可以打包吗？", "¿Es para llevar?", "识别卡；主动说可用 Para llevar, por favor。"),
        ("U8 酒店整合：我已经预订了两晚。", "Ya he reservado dos noches.", ""),
        ("U8 酒店整合：我还没付钱。", "Todavía no he pagado.", ""),
        ("U8 酒店整合：房间很吵，我睡不好。", "La habitación es muy ruidosa y no duermo bien.", ""),
        ("U8 酒店整合：可以换一间房吗？", "¿Me puede cambiar de habitación?", "高频酒店求助。"),
        ("U8 城市整合：这里附近有 ATM 吗？", "¿Hay un cajero por aquí?", "LatAm/旅行高频；避免重复 v047 的 farmacia。"),
        ("U8 城市整合：这里走路十分钟。", "Está a diez minutos caminando.", "LatAm 口语常用 caminando。"),
        ("U8 城市整合：往前走两个街区。", "Siga derecho dos cuadras.", "U6 拉美问路回收。"),
        ("U8 城市整合：在拐角左转。", "Doble a la izquierda en la esquina.", ""),
        ("U8 旅行偏好：我不喜欢太游客化的地方。", "No me gustan los lugares muy turísticos.", ""),
        ("U8 旅行偏好：我喜欢有烟火气的地方。", "Me gustan los lugares con mucha vida.", "自然表达，不直译“烟火气”。"),
        ("U8 旅行偏好：我喜欢晚上出去走走。", "Me gusta salir a caminar por la noche.", ""),
        ("U8 旅行偏好：我喜欢坐在露台上喝点东西。", "Me gusta tomar algo en una terraza.", ""),
    ], "u8_review_03 u8_review_04", "review_bridge latam_travel_upgrade", "integrated_phrase")

    add_contrast(b, "U8 辨析：¿Dónde está...? 还是 ¿Dónde hay...? 问“哪里有 ATM”？", "¿Dónde hay un cajero?", "不知道是否存在/哪里有，用 hay。", "u8_review_06")
    add_contrast(b, "U8 辨析：¿Dónde está...? 还是 ¿Dónde hay...? 问“我的酒店在哪里”？", "¿Dónde está mi hotel?", "具体已知地点的位置，用 estar。", "u8_review_06")
    add_contrast(b, "U8 辨析：“我住在市中心”用 en 还是 a？", "Vivo en el centro.", "静态位置用 en。", "u8_review_06")
    add_contrast(b, "U8 辨析：“我去市中心”用 en 还是 a?", "Voy al centro.", "方向/目的地用 a；a + el = al。", "u8_review_06")
    add_contrast(b, "U8 辨析：“已经”与“还没有”：ya / todavía no 怎么配？", "Ya he reservado. / Todavía no he pagado.", "两个都是 U7 旅行经历/准备的核心时间标记。", "u8_review_06")
    return b


def build_u9():
    b = Builder(
        "anki_v050",
        "anki_v050_nvh_u9_prebuild",
        "Spanish::Nos vemos hoy::U9 Caminando",
        "NVH U9 prebuild: clothing, comparison, reflexives, advice, weather, estar + gerundio",
    )
    add_vocab(b, [
        ("T恤；连冠词", "la camiseta", ""),
        ("衬衫；连冠词", "la camisa", ""),
        ("毛衣；连冠词", "el jersey", "西班牙教材常见；拉美很多地方也说 suéter。"),
        ("毛衣；拉美常见；连冠词", "el suéter", "Aula América 对照补充。"),
        ("夹克；连冠词", "la chaqueta", ""),
        ("外套；连冠词", "el abrigo", ""),
        ("裤子；复数；连冠词", "los pantalones", ""),
        ("牛仔裤；连冠词", "los pantalones vaqueros", "西班牙常见；拉美常说 los jeans。"),
        ("牛仔裤；拉美常见；连冠词", "los jeans", "Aula América/LatAm 对照补充。"),
        ("短裤；连冠词", "los shorts", "拉美旅行实用。"),
        ("裙子；连冠词", "la falda", ""),
        ("袜子；连冠词", "los calcetines", "西班牙常见；拉美很多地方说 medias。"),
        ("袜子；拉美常见；连冠词", "las medias", "Aula América 对照补充。"),
        ("登山靴；连冠词", "las botas de montaña", ""),
        ("鞋；连冠词", "los zapatos", ""),
        ("凉鞋；连冠词", "las sandalias", ""),
        ("帽子/毛线帽；连冠词", "el gorro", ""),
        ("帽子；遮阳帽；连冠词", "el sombrero", ""),
        ("太阳镜；连冠词", "las gafas de sol", "西班牙常见。"),
        ("太阳镜；拉美常见；连冠词", "los lentes de sol", "LatAm travel upgrade。"),
        ("背包；连冠词", "la mochila", ""),
        ("雨伞；连冠词", "el paraguas", ""),
        ("防晒霜；连冠词", "la crema solar", "西班牙常见；拉美也常说 protector solar。"),
        ("防晒；拉美常见；连冠词", "el protector solar", "Aula América 对照补充。"),
    ], "u9_block_01")

    add_vocab(b, [
        ("棉；连冠词", "el algodón", ""),
        ("羊毛；连冠词", "la lana", ""),
        ("皮革；连冠词", "el cuero", ""),
        ("木头；连冠词", "la madera", ""),
        ("亚麻；连冠词", "el lino", ""),
    ], "u9_block_01")

    add_pairs(b, [
        ("这件 T 恤是棉的。", "Esta camiseta es de algodón.", ""),
        ("这双靴子是皮的。", "Estas botas son de cuero.", ""),
        ("这件毛衣是羊毛的。", "Este jersey es de lana.", ""),
        ("我要带一件轻便的夹克。", "Voy a llevar una chaqueta ligera.", ""),
        ("我需要舒适的鞋。", "Necesito zapatos cómodos.", ""),
        ("你要带什么衣服？", "¿Qué ropa vas a llevar?", ""),
        ("我去山里，所以要带外套。", "Voy a la montaña, así que tengo que llevar un abrigo.", ""),
        ("我去海边，所以要带太阳镜。", "Voy a la playa, así que tengo que llevar lentes de sol.", ""),
        ("这条蓝色裤子很舒服。", "Estos pantalones azules son muy cómodos.", ""),
        ("这双棕色靴子很贵。", "Estas botas marrones son muy caras.", ""),
    ], "u9_block_01")

    for zh, es in [
        ("白色的", "blanco/blanca"), ("黑色的", "negro/negra"), ("红色的", "rojo/roja"),
        ("黄色的", "amarillo/amarilla"), ("蓝色的", "azul"), ("绿色的", "verde"),
        ("灰色的", "gris"), ("棕色的", "marrón"), ("橙色的", "naranja"), ("粉色的", "rosa"),
    ]:
        b.add(f"颜色：{zh}", es, "blanco/negro/rojo/amarillo 分阴阳；多数其他颜色不分阴阳但有复数。", "nvh_core u9_block_01 color")

    add_pairs(b, [
        ("旅馆比酒店便宜。", "Los albergues son más baratos que los hoteles.", ""),
        ("酒店比旅馆更舒服。", "Los hoteles son más cómodos que los albergues.", ""),
        ("背包比行李箱更适合徒步。", "Una mochila es mejor que una maleta para caminar.", ""),
        ("四月游客比七月少。", "En abril hay menos turistas que en julio.", ""),
        ("这条路线和那条一样漂亮。", "Esta ruta es tan bonita como esa.", ""),
        ("这个月是最推荐的月份。", "Este es el mes más recomendable.", ""),
        ("最大的问题是高原反应。", "El mayor problema es el soroche.", "Peru/Andes 旅行实用。"),
        ("这家酒店比那家更好。", "Este hotel es mejor que ese.", ""),
        ("雨天徒步更糟。", "Caminar con lluvia es peor.", ""),
    ], "u9_block_02")

    add_pairs(b, [
        ("这件夹克比那件轻。", "Esta chaqueta es más ligera que esa.", ""),
        ("这双鞋不如那双舒服。", "Estos zapatos son menos cómodos que esos.", ""),
        ("这条路线比那条长。", "Esta ruta es más larga que esa.", ""),
        ("这座城市比我的城市更热。", "Esta ciudad es más calurosa que mi ciudad.", ""),
        ("今天比昨天冷。", "Hoy hace más frío que ayer.", ""),
        ("这家酒店没有那家贵。", "Este hotel es menos caro que ese.", ""),
        ("这件衬衫和那件一样漂亮。", "Esta camisa es tan bonita como esa.", ""),
        ("这个背包和那个一样实用。", "Esta mochila es tan práctica como esa.", ""),
        ("我走得比你多。", "Yo camino más que tú.", "verbo + más que。"),
        ("我睡得比你少。", "Yo duermo menos que tú.", "verbo + menos que。"),
        ("这里游客和那里一样多。", "Aquí hay tantos turistas como allí.", "tanto/a/os/as + nombre + como。"),
        ("这是一年中最好的季节。", "Es la mejor época del año.", "mejor 是 bueno 的比较级/最高级形式。"),
    ], "u9_block_02", "nvh_core latam_travel_upgrade", "comparison_phrase")

    add_pairs(b, [
        ("我早上六点起床。", "Me levanto a las seis de la mañana.", ""),
        ("我洗脸。", "Me lavo la cara.", ""),
        ("我刷牙。", "Me lavo los dientes.", ""),
        ("我穿上舒适的衣服。", "Me pongo ropa cómoda.", ""),
        ("我们坐下来休息。", "Nos sentamos para descansar.", ""),
        ("我们很早睡。", "Nos acostamos temprano.", ""),
        ("我晚上洗澡。", "Me ducho por la noche.", ""),
        ("我需要洗手。", "Necesito lavarme las manos.", "反身代词接 infinitivo 后。"),
        ("我不想现在洗澡。", "No quiero ducharme ahora.", ""),
        ("我们累了就休息一下。", "Cuando nos cansamos, hacemos una pausa.", ""),
    ], "u9_block_03")

    for inf, yo, tu, el in [
        ("levantarse", "me levanto", "te levantas", "se levanta"),
        ("lavarse", "me lavo", "te lavas", "se lava"),
        ("ponerse", "me pongo", "te pones", "se pone"),
        ("sentarse", "me siento", "te sientas", "se sienta"),
        ("acostarse", "me acuesto", "te acuestas", "se acuesta"),
        ("ducharse", "me ducho", "te duchas", "se ducha"),
    ]:
        b.add(f"`{inf}`：yo / tú / él 三个高频形式", f"{yo} / {tu} / {el}", "只要求识别和使用常见人称，不做全表背诵。", "nvh_core u9_block_03 grammar reflexive")

    add_pairs(b, [
        ("你喜欢这条裙子吗？", "¿Te gusta esta falda?", ""),
        ("这件红色的呢？", "¿Y esta roja?", "省略 falda/camiseta 等已知名词。"),
        ("我选这条裤子。", "Elijo estos pantalones.", ""),
        ("那件夹克更轻。", "Esa chaqueta es más ligera.", ""),
        ("这些鞋很舒服。", "Estos zapatos son muy cómodos.", ""),
        ("那些靴子太贵了。", "Esas botas son demasiado caras.", ""),
        ("这是什么？", "¿Qué es esto?", "不知道名称时用 esto。"),
        ("那是什么？", "¿Qué es eso?", ""),
        ("我喜欢这个，但是那个不喜欢。", "Me gusta esto, pero eso no.", ""),
    ], "u9_block_04")

    add_pairs(b, [
        ("我要这件。", "Me llevo esta.", "购物场景：前面已知是 prenda/falda/camiseta。"),
        ("我要这双。", "Me llevo estos.", "购物场景：前面已知是 zapatos/lentes 等复数阳性。"),
        ("这件有 L 码吗？", "¿Tiene esta en talla L?", "Aula América 购物补充。"),
        ("这双有黑色的吗？", "¿Tiene estos en negro?", ""),
        ("我可以试一下吗？", "¿Me lo puedo probar?", "衣物购物高频；lo 指前面提到的单数阳性物。"),
        ("我可以试这件吗？", "¿Me puedo probar esta?", ""),
        ("太大了。", "Me queda muy grande.", "衣物试穿高频。"),
        ("太小了。", "Me queda muy chico.", "LatAm 常用 chico；pequeño 也可以。"),
        ("很合适。", "Me queda bien.", ""),
        ("我只是看看，谢谢。", "Solo estoy mirando, gracias.", "逛店高频防打扰句。"),
    ], "u9_block_04", "aula_america_alignment latam_travel_upgrade", "shopping_phrase")

    add_pairs(b, [
        ("建议：最好早点出发。", "Es mejor salir temprano.", ""),
        ("建议：建议带水。", "Se recomienda llevar agua.", ""),
        ("建议：最好穿舒服的鞋。", "Es mejor ponerse zapatos cómodos.", ""),
        ("建议：不需要带食物。", "No es necesario llevar comida.", ""),
        ("建议：应该提前预订。", "Conviene hacer la reserva con anticipación.", "旅行高频。"),
        ("建议：建议先在库斯科待几天。", "Se recomienda pasar unos días en Cusco.", ""),
        ("建议：最好慢慢走。", "Es mejor caminar despacio.", ""),
        ("建议：应该带防晒。", "Conviene llevar protector solar.", "LatAm travel upgrade。"),
        ("建议：应该喝很多水。", "Conviene beber mucha agua.", ""),
        ("建议：不建议带小孩。", "No conviene llevar niños.", ""),
        ("建议：最好打车。", "Es mejor ir en taxi.", "U6 交通回收。"),
        ("建议：如果下雨，最好别走路。", "Si llueve, es mejor no caminar.", ""),
    ], "u9_block_05")

    add_pairs(b, [
        ("去高海拔地区，建议先休息。", "Para ir a un lugar alto, se recomienda descansar primero.", ""),
        ("去山里，应该带一件外套。", "Para ir a la montaña, conviene llevar una chaqueta.", ""),
        ("去海边，不需要带很多衣服。", "Para ir a la playa, no es necesario llevar mucha ropa.", ""),
        ("如果很热，最好带水。", "Si hace mucho calor, es mejor llevar agua.", ""),
        ("如果有雾，最好慢慢走。", "Si hay niebla, es mejor caminar despacio.", ""),
        ("如果下雨，建议穿防水夹克。", "Si llueve, se recomienda llevar una chaqueta impermeable.", ""),
        ("如果很远，最好坐车。", "Si está muy lejos, es mejor ir en coche.", ""),
        ("如果只是市中心，走路就可以。", "Si es solo el centro, se puede ir caminando.", ""),
    ], "u9_block_05", "latam_travel_upgrade", "advice_phrase")

    add_pairs(b, [
        ("我正在等导游。", "Estoy esperando al guía.", ""),
        ("我们正在走路。", "Estamos caminando.", ""),
        ("她正在拍照。", "Está tomando fotos.", ""),
        ("他们正在参观一座印加古城。", "Están visitando una antigua ciudad inca.", ""),
        ("你正在读什么？", "¿Qué estás leyendo?", ""),
        ("我正在洗澡。", "Me estoy duchando.", ""),
        ("我正在洗澡。另一种说法。", "Estoy duchándome.", "代词可放在 estar 前，也可贴在 gerundio 后。"),
        ("我们正在去超市。", "Estamos yendo al supermercado.", ""),
        ("他正在睡觉。", "Está durmiendo.", ""),
        ("你正在点什么吃的？", "¿Qué estás pidiendo para comer?", ""),
    ], "u9_block_06")

    add_pairs(b, [
        ("今天天气怎么样？", "¿Qué tiempo hace hoy?", ""),
        ("天气很好。", "Hace buen tiempo.", ""),
        ("天气不好。", "Hace mal tiempo.", ""),
        ("晴天。", "Hace sol.", ""),
        ("很热。", "Hace mucho calor.", ""),
        ("很冷。", "Hace mucho frío.", ""),
        ("风很大。", "Hace mucho viento.", ""),
        ("多云。", "Está nublado.", ""),
        ("有雾。", "Hay niebla.", ""),
        ("下雨。", "Llueve.", ""),
        ("雪下得很大。", "Nieva mucho.", ""),
        ("现在正在下雨。", "Está lloviendo.", "旅行中非常实用的进行时。"),
        ("三十度。", "Hace treinta grados.", ""),
        ("零下五度。", "Hace cinco grados bajo cero.", ""),
        ("如果下雨，我们坐出租车。", "Si llueve, vamos en taxi.", ""),
    ], "u9_block_06")

    add_contrast(b, "“这件 T 恤是棉的”：材料前用什么介词？", "Es de algodón.", "材料用 de。", "u9_block_01")
    add_contrast(b, "“这些黄色 T 恤”：amarillo 怎么变？", "estas camisetas amarillas", "amarillo 分阴阳和单复数。", "u9_block_01")
    add_contrast(b, "“这些蓝色 T 恤”：azul 怎么变？", "estas camisetas azules", "azul 不分阴阳，但有复数。", "u9_block_01")
    add_contrast(b, "“我洗手”不能说 lavo mis manos，自然说？", "Me lavo las manos.", "身体部位常用定冠词，反身代词说明是谁的。", "u9_block_03")
    add_contrast(b, "“认识 Shakira”：conocer 后面为什么有 a？", "Conozco a Shakira.", "人作直接宾语时通常加 personal a。", "u9_block_03")
    add_contrast(b, "“我有十个表兄弟姐妹”：tener 后面加 personal a 吗？", "Tengo diez primos.", "tener 是常见例外，不加 personal a。", "u9_block_03")
    add_contrast(b, "“我正在洗澡”：代词可以放两个位置，说出两个。", "Me estoy duchando. / Estoy duchándome.", "两种都自然。", "u9_block_06")
    add_contrast(b, "“天气多云”：hacer 还是 estar？", "Está nublado.", "nublado 是状态形容词，用 estar。", "u9_block_06")
    return b


def write_tsv(builder):
    path = OUT / f"{builder.name}.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(builder.rows)
    return path


def now_ms():
    return int(time.time() * 1000)


def guid_for(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def make_apkg(rows, name):
    apkg = OUT / f"{name}.apkg"
    db = OUT / f"{name}.anki2"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executescript("""
CREATE TABLE col (
    id integer primary key,
    crt integer not null,
    mod integer not null,
    scm integer not null,
    ver integer not null,
    dty integer not null,
    usn integer not null,
    ls integer not null,
    conf text not null,
    models text not null,
    decks text not null,
    dconf text not null,
    tags text not null
);
CREATE TABLE notes (
    id integer primary key,
    guid text not null,
    mid integer not null,
    mod integer not null,
    usn integer not null,
    tags text not null,
    flds text not null,
    sfld integer not null,
    csum integer not null,
    flags integer not null,
    data text not null
);
CREATE TABLE cards (
    id integer primary key,
    nid integer not null,
    did integer not null,
    ord integer not null,
    mod integer not null,
    usn integer not null,
    type integer not null,
    queue integer not null,
    due integer not null,
    ivl integer not null,
    factor integer not null,
    reps integer not null,
    lapses integer not null,
    left integer not null,
    odue integer not null,
    odid integer not null,
    flags integer not null,
    data text not null
);
CREATE TABLE revlog (
    id integer primary key,
    cid integer not null,
    usn integer not null,
    ease integer not null,
    ivl integer not null,
    lastIvl integer not null,
    factor integer not null,
    time integer not null,
    type integer not null
);
CREATE TABLE graves (
    usn integer not null,
    oid integer not null,
    type integer not null
);
""")
    model_id = 1700000000001
    deck_ids = {}
    decks = {}
    for i, deck in enumerate(dict.fromkeys(r["deck"] for r in rows), start=1):
        did = 1700001000000 + i
        deck_ids[deck] = did
        decks[str(did)] = {
            "id": did, "name": deck, "desc": "", "dyn": 0, "collapsed": False,
            "browserCollapsed": False, "conf": 1, "extendNew": 10, "extendRev": 50,
            "mod": int(time.time()), "usn": -1, "newToday": [0, 0], "revToday": [0, 0],
            "lrnToday": [0, 0], "timeToday": [0, 0]
        }
    decks["1"] = {"id": 1, "name": "Default", "desc": "", "dyn": 0, "collapsed": False,
                  "browserCollapsed": False, "conf": 1, "extendNew": 10, "extendRev": 50,
                  "mod": int(time.time()), "usn": -1, "newToday": [0, 0], "revToday": [0, 0],
                  "lrnToday": [0, 0], "timeToday": [0, 0]}
    models = {
        str(model_id): {
            "id": model_id,
            "name": "Spanish Basic Travel",
            "type": 0,
            "mod": int(time.time()),
            "usn": -1,
            "sortf": 0,
            "did": None,
            "tmpls": [{
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Back}}<br><br><div style='font-size:85%;color:#555'>{{Extra}}</div>",
                "did": None,
                "bqfmt": "", "bafmt": ""
            }],
            "flds": [
                {"name": "Front", "ord": 0, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "description": "", "plainText": False, "collapsed": False, "excludeFromSearch": False, "tag": None},
                {"name": "Back", "ord": 1, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "description": "", "plainText": False, "collapsed": False, "excludeFromSearch": False, "tag": None},
                {"name": "Extra", "ord": 2, "sticky": False, "rtl": False, "font": "Arial", "size": 16, "description": "", "plainText": False, "collapsed": False, "excludeFromSearch": False, "tag": None},
            ],
            "css": ".card { font-family: Arial; font-size: 20px; text-align: left; color: black; background-color: white; line-height: 1.35; }",
            "latexPre": "", "latexPost": "", "latexsvg": False, "req": [[0, "any", [0]]],
            "tags": [], "vers": []
        }
    }
    conf = {"nextPos": 1, "estTimes": True, "activeDecks": [1], "sortType": "noteFld", "timeLim": 0}
    dconf = {"1": {"id": 1, "name": "Default", "mod": 0, "usn": 0, "maxTaken": 60,
                   "autoplay": True, "timer": 0, "replayq": True, "new": {"perDay": 20, "delays": [1, 10], "ints": [1, 4, 0], "initialFactor": 2500, "order": 1, "bury": True},
                   "rev": {"perDay": 200, "ease4": 1.3, "fuzz": 0.05, "minSpace": 1, "ivlFct": 1, "maxIvl": 36500, "bury": True},
                   "lapse": {"delays": [10], "mult": 0, "minInt": 1, "leechFails": 8, "leechAction": 0}}}
    ts = int(time.time())
    cur.execute("insert into col values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (1, ts, ts, now_ms(), 11, 0, 0, 0, json.dumps(conf), json.dumps(models),
                 json.dumps(decks), json.dumps(dconf), json.dumps({})))
    for idx, row in enumerate(rows, start=1):
        nid = now_ms() + idx
        cid = nid + 100000
        flds = "\x1f".join([row["front"], row["back"], row["extra"]])
        csum = int(hashlib.sha1(row["front"].encode("utf-8")).hexdigest()[:8], 16)
        cur.execute("insert into notes values (?,?,?,?,?,?,?,?,?,?,?)",
                    (nid, guid_for(row["front"] + row["back"]), model_id, ts, -1,
                     " " + row["tags"] + " ", flds, row["front"], csum, 0, ""))
        cur.execute("insert into cards values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (cid, nid, deck_ids[row["deck"]], 0, ts, -1, 0, 0, idx, 0, 2500, 0, 0, 0, 0, 0, 0, ""))
    con.commit()
    con.close()
    with zipfile.ZipFile(apkg, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(db, "collection.anki2")
        z.writestr("media", "{}")
    db.unlink()
    return apkg


def write_manifest(builder, tsv, apkg):
    manifest = {
        "name": builder.name,
        "version": builder.version,
        "deck": builder.deck,
        "note_count": len(builder.rows),
        "skipped_duplicate_count": len(builder.skipped),
        "created_utc": "2026-09-05",
        "scope": builder.scope,
        "review_pack": builder.review,
        "dedupe_baseline": "anki_v047_nvh_u6_prebuild.tsv",
        "fields": FIELDS,
        "source_layers": ["nvh_core", "aula_america_alignment", "latam_travel_upgrade", "error_review"],
        "ordering": "lesson block order; basic vocabulary -> structures -> collocations -> phrases -> scenario Q&A -> contrasts -> output",
        "files": [str(tsv), str(apkg)],
    }
    path = OUT / f"{builder.name}.manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def make_bundle(files, name):
    path = OUT / f"{name}.zip"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.name)
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    builders = [build_u7(), build_u8(), build_u9()]
    all_files = []
    all_rows = []
    summaries = []
    for b in builders:
        tsv = write_tsv(b)
        apkg = make_apkg(b.rows, b.name)
        manifest = write_manifest(b, tsv, apkg)
        all_files.extend([apkg, tsv, manifest])
        all_rows.extend(b.rows)
        summaries.append({"name": b.name, "notes": len(b.rows), "skipped_duplicates": len(b.skipped)})

    combined_name = "anki_v048_v050_nvh_travel_pack"
    combined_tsv = OUT / f"{combined_name}.tsv"
    with combined_tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(all_rows)
    combined_apkg = make_apkg(all_rows, combined_name)
    combined_manifest = {
        "name": combined_name,
        "versions": ["anki_v048", "anki_v049", "anki_v050"],
        "deck": "Spanish::Nos vemos hoy::Travel prebuild U7-U9",
        "note_count": len(all_rows),
        "created_utc": "2026-09-05",
        "dedupe_baseline": "anki_v047_nvh_u6_prebuild.tsv",
        "components": summaries,
        "source_layers": ["nvh_core", "aula_america_alignment", "latam_travel_upgrade", "error_review"],
        "ordering": "U7 blocks, U8 Mirador review blocks, U9 blocks",
        "fields": FIELDS,
        "files": [str(combined_tsv), str(combined_apkg)],
    }
    combined_manifest_path = OUT / f"{combined_name}.manifest.json"
    combined_manifest_path.write_text(json.dumps(combined_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    all_files.extend([combined_apkg, combined_tsv, combined_manifest_path])
    bundle = make_bundle(all_files, "anki_v048_v050_nvh_travel_prebuild_bundle")
    summary = {"components": summaries, "combined_notes": len(all_rows), "bundle": str(bundle), "output_dir": str(OUT)}
    (OUT / "build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
