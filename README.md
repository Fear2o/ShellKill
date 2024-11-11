# 🐚 **ShellKill** 💀🔥

## Overview 📖
**ShellKill** is a Python tool designed to upload a **web shell** to a target server and trigger it using various **evasion techniques** to bypass file upload restrictions. A **web shell** is a script that provides remote access and control over a web server. By uploading a web shell, an attacker can execute commands on the target server, manipulate files, and potentially escalate privileges.

The tool also supports **automatic retries**, file upload validation, and vulnerability scanning for common web vulnerabilities such as **File Upload issues, LFI/RFI, XSS**, and SQL Injection.

> **Warning:** This tool can potentially cause significant damage if misused. Only use it in controlled environments where explicit permission has been granted. 🚨

![GitHub stars](https://img.shields.io/github/stars/Fear2o/ShellKill?style=social)
![Build Status](https://img.shields.io/github/workflow/status/Fear2o/ShellKill/CI)
![License](https://img.shields.io/github/license/Fear2o/ShellKill)
![Contributors](https://img.shields.io/github/contributors/Fear2o/ShellKill)

### 🚀 **Key Features:**

- **Shell File Upload**: Easily upload a web shell to a target server via a specified URL. ⚡
- **Retries and Error Handling**: Automatic retries on failure with detailed error logging for easy debugging. 🔄
- **Evasion Techniques**: Bypass file upload restrictions using creative methods like file renaming and base64 encoding. 🛡️
- **Vulnerability Scanning**: Automatically scan the target URL for common vulnerabilities like **File Upload issues**, **LFI/RFI**, **XSS**, and **SQL Injection**. 🔍
- **Customizable**: Configure retry count, proxies, and timeout settings with ease. 🛠️

---

## 🚨 **Prerequisites** 🛠️

Before you begin, make sure you have:

- **Python 3.6+**: WebShellUploader is built for Python 3.6 and above. 🔑
- **Required Libraries**: Install the necessary libraries using `pip`:
    ```bash
    pip install requests validators
    ```

---

## 📝 **Usage**

### Command-Line Arguments 🎯

- `target_url`: Target URL of the server you want to test. (e.g., `http://example.com`)
- `shell_file_path`: Path to the web shell you want to upload. 🗂️
- `upload_url`: The upload endpoint where the file should be uploaded. 📤
- `--proxies`: Optional argument to specify proxies. (e.g., `--proxies http://127.0.0.1:8080`)
- `--max_retries`: Set the maximum number of retries for the upload (default: `5`). 🔄
- `--evasion_techniques`: Enable or disable evasion techniques. Default is `True`. 🕶️
- `--timeout`: Set the timeout for requests in seconds (default: `10`). ⏳

### 🖥️ **Example Command**

```bash
python webshell_uploader.py http://example.com /path/to/shell.php http://example.com/upload --max_retries 5 --evasion_techniques True --timeout 10
```


## 📊 Logging & Reports 📜

All actions performed by **ShellKill** are logged into a rotating log file named upload_log.txt. Here's an example of what the logs might look like:

2024-11-10 12:34:56,789 - INFO - Target URL http://example.com is reachable.
2024-11-10 12:35:00,123 - INFO - Shell file /path/to/shell.php is valid and readable.
2024-11-10 12:35:05,456 - INFO - Attempting upload with renamed shell: shell_1234.php.
2024-11-10 12:35:10,789 - ERROR - Request failed (Attempt 1): Timeout error.
2024-11-10 12:35:15,123 - INFO - Shell uploaded successfully: /path/to/shell.php.


## 📈 How to Contribute 💡

We welcome contributions to **ShellKill!** If you find bugs, have ideas for features, or want to help improve the project, please feel free to:

1. **Fork the repo 🍴**
2. **Create a feature branch 🌱**
3. **Submit a pull request 🚀**
We highly appreciate all contributions and feedback from the community!


## ⭐ **Give It a Star!**

If you found this tool useful, please give it a ⭐ and **follow** for future updates. 🚀 Your support helps improve the tool and motivates the development of more awesome features! 

[Star this repository on GitHub](https://github.com/Fear2o/ShellKill) ⭐


## **📌 Disclaimer ⚠️**

This tool is for **educational purposes only**. You must have **explicit permission** to test any web server. The author is not responsible for any illegal use or actions taken using this tool. **Use responsibly and ethically!** 💻


## **📚 License 🛡️**

This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/Fear2o/ShellKill/blob/main/LICENSE) 
file for more details. 📝


## **🔔 Stay Updated 📰**

- Follow me on [GitHub](https://github.com/Fear2o) for the latest updates!

- Join the discussion and contribute to making **ShellKill** even better. 👥

### **🏅 Thank you for your support! 🙌**
Keep hacking responsibly and stay awesome! 😎

***____________________________________________________***

*Crafted by Fear.io*
