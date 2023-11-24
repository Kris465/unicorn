import asyncio
from domain.file_tools import read, write
from translator.connector import Translator


class TrManager:
    def __init__(self, title, language, option):
        self.title = title
        self.language = language
        self.option = option

    async def translate(self):
        if self.option == 1:
            await self.translate_all()
        elif self.option == 2:
            await self.translate_from()
        elif self.option == 3:
            await self.translate_from_to()

    async def translate_all(self):
        full_chapters = {}
        project = await asyncio.to_thread(read, f"{self.title}")
        for chapter in project:
            text = project[chapter]
            tr_txt = await self.translate_text(text)
            full_chapters[chapter] = [{"origin": text}, {"translation": tr_txt}]
        await write(self.title + "_translation", full_chapters, self.language)

    async def translate_from(self):
        start_chapter = int(input("From: "))
        full_chapters = {}
        project = await asyncio.to_thread(read, f"{self.title}")
        for chapter in project:
            if chapter >= start_chapter:
                text = project[chapter]
                tr_txt = await self.translate_text(text)
                full_chapters[chapter] = [{"origin": text}, {"translation": tr_txt}]
        await write(self.title + "_translation", full_chapters, self.language)

    async def translate_from_to(self):
        start_chapter = int(input("From: "))
        last_chapter = int(input("To: "))
        full_chapters = {}
        project = await asyncio.to_thread(read, f"{self.title}")
        for chapter in project:
            if start_chapter <= chapter <= last_chapter:
                text = project[chapter]
                tr_txt = await self.translate_text(text)
                full_chapters[chapter] = [{"origin": text}, {"translation": tr_txt}]
        await write(self.title + "_translation", full_chapters, self.language)

    async def translate_text(self, text):
        max_length = 10000
        substrings = []
        sign = self.get_sign(self.language)

        while len(text) > max_length:
            index = text.rfind(sign, 0, max_length)
            if index == -1:
                index = max_length
            substrings.append(text[:index+1])
            text = text[index+1:]

        if len(text) > 0:
            substrings.append(text)

        translator = Translator()
        tr_txt = ""
        for string in substrings:
            part = await translator.translate(string, self.language)
            if part is not None:
                tr_txt += part.text
            else:
                break

        return tr_txt

    def get_sign(self, language):
        if language == "zh":
            return "。"
        else:
            return "."
