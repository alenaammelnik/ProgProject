import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_fetch_tasks(driver):
    """
    Тест для проверки загрузки задач на странице.
    
    Эта функция ожидает появления элемента задач на странице и проверяет,
    отображается ли начальная задача "Learn Flask".
    
    Args:
        driver (webdriver.Chrome): Экземпляр Selenium WebDriver.
        
    Raises:
        AssertionError: Если начальная задача не найдена.
    """
    tasks = driver.find_element(By.ID, "tasks")
    assert "Learn Flask" in tasks.text, "Initial task not found"
    print("test_fetch_tasks passed")

def test_add_task(driver):
    """
    Тест для проверки возможности добавления новой задачи.
    
    Эта функция заполняет форму для добавления новой задачи и отправляет ее.
    Затем она ожидает обновления элемента задач и проверяет, отображается ли новая задача.
    
    Args:
        driver (webdriver.Chrome): Экземпляр Selenium WebDriver.
        
    Raises:
        AssertionError: Если новая задача не найдена в списке задач.
    """
    title_input = driver.find_element(By.ID, "title")
    description_input = driver.find_element(By.ID, "description")
    author_input = driver.find_element(By.ID, "author")
    submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

    title_input.send_keys("Test Task")
    description_input.send_keys("Test Description")
    author_input.send_keys("Test Author")
    submit_button.click()

    time.sleep(1)  # даем время серверу обработать запрос и обновить страницу

    tasks = driver.find_element(By.ID, "tasks")
    assert "Test Task" in tasks.text, "New task not found in task list"
    print("test_add_task passed")

def test_mark_task_done(driver):
    """
    Тест для проверки возможности отметки задачи как выполненной.
    
    Эта функция находит задачу и отмечает ее как выполненную.
    Затем она ожидает обновления элемента задач и проверяет, изменилось ли состояние задачи.
    
    Args:
        driver (webdriver.Chrome): Экземпляр Selenium WebDriver.
        
    Raises:
        AssertionError: Если задача не была отмечена как выполненная.
    """
    tasks = driver.find_element(By.ID, "tasks")
    button = tasks.find_element(By.XPATH, "//li[contains(text(), 'Test Task')]/button[text()='Mark as Done']")
    button.click()

    time.sleep(1)  # даем время серверу обработать запрос и обновить страницу

    tasks = driver.find_element(By.ID, "tasks")
    assert "true" in tasks.text, "Task not marked as done"
    print("test_mark_task_done passed")

def test_delete_task(driver):
    """
    Тест для проверки возможности удаления задачи.
    
    Эта функция находит задачу и удаляет ее.
    Затем она ожидает обновления элемента задач и проверяет, была ли задача удалена.
    
    Args:
        driver (webdriver.Chrome): Экземпляр Selenium WebDriver.
        
    Raises:
        AssertionError: Если задача не была удалена.
    """
    tasks = driver.find_element(By.ID, "tasks")
    button = tasks.find_element(By.XPATH, "//li[contains(text(), 'Test Task')]/button[text()='Delete']")
    button.click()

    time.sleep(1)  # даем время серверу обработать запрос и обновить страницу

    tasks = driver.find_element(By.ID, "tasks")
    assert "Test Task" not in tasks.text, "Task not deleted"
    print("test_delete_task passed")

if __name__ == "__main__":
    driver = webdriver.Chrome()  
    driver.get("http://127.0.0.1:5000") 

    try:
        test_fetch_tasks(driver)
        test_add_task(driver)
        test_mark_task_done(driver)
        test_delete_task(driver)
    finally:
        driver.quit()


