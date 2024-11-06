from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from config import get_chrome_options, TIMEOUT

def capture_result(browser):
    try:
        WebDriverWait(browser, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "N")]/b'))
        )
        elements = {
            "cpf": '//span[contains(text(), "N")]/b',
            "name": '//span[contains(text(), "Nome:")]/b',
            "birth_date": '//span[contains(text(), "Data de Nascimento:")]/b',
            "situation": '//span[contains(text(), "Situação Cadastral:")]/b',
            "subscribe_date": '//span[contains(text(), "Data da Inscrição:")]/b',
            "check_digit": '//span[contains(text(), "Digito Verificador:")]/b',
            "consult_hour": '//span[contains(text(), "Comprovante emitido às:")]/b[1]',
            "consult_date": '//span[contains(text(), "Comprovante emitido às:")]/b[2]',
            "control_code": '//span[contains(text(), "Código de controle do comprovante:")]/b',
        }
        result = {key: browser.find_element(By.XPATH, xpath).text for key, xpath in elements.items()}
        # result["death_year"] = None
        # if result["situation"] == "TITULAR FALECIDO":
        #     death_year_element = browser.find_element(By.XPATH, "//span[contains(text(),'Ano de óbito:')]/b")
        #     result["death_year"] = death_year_element.text
        #     return result
        # else:
        return result
    except NoSuchElementException:
        try:
            divergent_birth_date = browser.find_element(By.XPATH, '//*[@id="content-core"]/div/div/div[1]/span')
            return "Divergent Birth date."
        except NoSuchElementException:
            try:
                incorrect_cpf = browser.find_element(By.XPATH, '//*[@id="content-core"]/div/div/div[1]/span/h4/text()[1]')
                return "Incorrect Cpf."
            except NoSuchElementException:
                pass
    return "The result was not found."

def scraping(cpf, birth_date):
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=get_chrome_options())
    browser.get("https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp")
    wait = WebDriverWait(browser, TIMEOUT)

    try:
        cpf_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtCPF"]')))
        cpf_input.send_keys(cpf)
        data_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtDataNascimento"]')))
        data_input.send_keys(birth_date)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="capsolver-solver-info" and text()="Captcha solved!"]')))
        botao = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_submit"]')))
        botao.click()
        response = capture_result(browser)
        return response
    except TimeoutException:
        return "Timeout error."
    finally:
        browser.delete_all_cookies
        browser.quit()
