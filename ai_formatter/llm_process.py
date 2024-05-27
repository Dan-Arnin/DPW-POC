import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
import yfinance as yf

# from langchain_groq import ChatGroq
load_dotenv("../.env")  # Adjust the path if necessary

# Access the key from the .env file
mistral_ai_key = os.getenv("MISTRAL_API_KEY")


def date_format_processor(date1, date2):
    llm = ChatMistralAI(
        api_key=mistral_ai_key,
        model_kwargs={"response_format": {"type": "json_object"}},
        model="open-mixtral-8x22b",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            (
                "user",
                """
            You will be given two dates, check if they are in the same format, DO NOT expect them to 
            be in the standard format like dd/mm/yy they can be in any format like dd Month Year.
            You are to compare the two dates and tell if they are in the same format.

            Here are a few examples for you to understand.

            Date 1: 02/04/2002 ; Date 2: 04/05/2034
            Format Same : YES

            Date 1: 02 May 2002 ; Date 2: 04 April 2034
            Format Same : YES

            Date 1 : May-June 2023 ; Date 2: April-August 2055
            Format Same : YES

            Date 1 : May-June 2023 ; Date 2: May 2023 June 2023
            Format Same : NO

            Now do the same for the below provided dates:

            Date 1: {date1}
            Date 2: {date2}

            A simple YES or NO is enought nothing else is required.Provide the data in JSON format only. REMEMBER TO COMPARE
            THE FORMATS ONLY, VALUES DONT MATTER. EVEN IF THE DATES ARE SAME AND FORMAT IS DIFFERENT ITS A NO.

            JSON format:
            "format" : "YES/NO"

            Provide the answer in the above JSON format nothing else is required""",
            ),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    format_check = chain.invoke({"date1": date1, "date2": date2})
    if format_check:
        format_check = json.loads(format_check)
        return format_check


def date_format_convertor(date_, format_):
    llm = ChatMistralAI(
        api_key=mistral_ai_key,
        model_kwargs={"response_format": {"type": "json_object"}},
        model="open-mixtral-8x22b",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            (
                "user",
                """
            You are a helpful assistant. 

            You will be given two dates date to be converted and a format date, both of which will be in a different format, You are to convert
            the first date to the format of the second date, as such you are required to deduce the format of 
            the second date and convert the format of the first other date. Keep in mind that the dates might not follow a standard template
            and can come in any varying format. Both the dates might not be the same, DO NOT GET CONFUSED AND GET THE DATES MIXED UP.

            Now analyze the format of the second date and change the format of the first date accordingly, DO NOT CHANGE THE VALUE.

            Date to be formatted: {date_}
            Format Date: {format_}
            
            SO basically change the format of {date_} to the format of {format_}. Do not copy the dates of {format_}

           Just provide the changed date. Provide the data in JSON format only. 

            JSON format:
            "format" : <new_date_format>

            Provide the answer in the above JSON format nothing else is required""",
            ),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    format_check = json.loads(chain.invoke({"date_": date_, "format_": format_}))
    return format_check


def currency_format_check(currency_1, currency_2):
    llm = ChatMistralAI(
        api_key=mistral_ai_key,
        model_kwargs={"response_format": {"type": "json_object"}},
        model="open-mixtral-8x22b",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            (
                "user",
                """
            You will be given two currencies. They might be the same or different countries
            Now analyze the currencies and state whether they are the same or different

            Currency 1 : {currency_1}
            Currency 2 : {currency_2}
            
            Just tell if they are the same. DO NOT LOOK AT THE 
            VALUE, JUST TELL IF THEY ARE THE CURRENCY FROM THE SAME COUNTRY OR NO
            If they are the same provide the following JSON:
            "same" : "Yes/No"

            Provide the answer in the above JSON format nothing else is required""",
            ),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    format_check = chain.invoke({"currency_1": currency_1, "currency_2": currency_2})
    print(format_check)
    format_check = json.loads(format_check)
    return format_check


def currency_exchange(from_currency, to_currency, amount):
    # Tickers for the currency exchange rate in Yahoo Finance format
    ticker = f"{from_currency}{to_currency}=X"
    # Fetch the exchange rate data
    data = yf.Ticker(ticker)
    # Get the current exchange rate
    exchange_rate = data.history(period="1d")["Close"].iloc[-1]
    # Convert the amount
    converted_amount = amount * exchange_rate
    return converted_amount


def currency_get_format(currency_1, currency_2):
    llm = ChatMistralAI(
        api_key=mistral_ai_key,
        model_kwargs={"response_format": {"type": "json_object"}},
        model="open-mixtral-8x22b",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            (
                "user",
                """
            You will be given two currencies. Analyze the currencies and provide 
            their standard currency format.

            <example>
            Currency 1 : $ 10
            Currency 2 : Rs. 100
     
            Output: 
            "currency_1" : "INR"
            "currency_2" : "USD"
     
            <example>
            Perform that for the below currencies
            
            Currency 1 : {currency_1}
            Currency 2 : {currency_2}
           
            JSON format:
            "currency1" : "standard_currency_format_1"
            "currency2" : "standard_currency_format_2"


            Provide the answer in the above JSON format nothing else is required. NO explanation is required ONLY PROVIDE JSON""",
            ),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    # format_check = json.loads(chain.invoke({"currency_1": currency_1, "currency_2": currency_2}))
    format_check = chain.invoke({"currency_1": currency_1, "currency_2": currency_2})
    return json.loads(format_check)
