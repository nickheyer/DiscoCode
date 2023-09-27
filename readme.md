# DiscoCode

Welcome to DiscoCode, a playful concoction of "Discord" and "Code"! 🎉 DiscoCode is a containerized code execution web server and a Discord bot that allows you to run code directly from Discord in over 25 languages!


<hr />
<br />


## General Requirements
Running the discord bot requires a [discord developer account](https://discord.com/developers/applications), and a bot created/invited (via your developer account) to your chosen discord server.


<br />


## Installation (Recommended Method)

### Linux (Fully Automated)

```bash 
curl https://raw.githubusercontent.com/nickheyer/DiscoCode/main/auto_install_update.sh -o auto_install_update.sh && sudo bash auto_install_update.sh
```

### Other Operating Systems (Windows, Mac, etc.)


##### Download Docker Image (Recommended - x86_64 Architecture) 

```bash
docker image pull nickheyer/discocode:latest
```
##### OR Download Docker Image (ARM64, aarch64 Architecture, ie: Raspberry-Pi, Mac M1, etc.) 

```bash
docker image pull nickheyer/discocode_rpi:latest
```
##### Run Docker Container

```bash
docker run -d -p 5454:5454 --name discocode nickheyer/discocode
```
##### The server within the docker container can be accessed locally at [http://127.0.0.1:5454](http://127.0.0.1:5454)

<hr />
<br />


## Installation From Source (Not Recommended)

### Prerequisites, Dependencies, and Requirements
**_NOTE:_**  Installation from source using Windows has been deprecated with the introduction of web-socket functionality, gevent, and other integral parts of this application that are not currently supported by Microsoft.

1. Python - Download and install Python [here](https://www.python.org/downloads/). Make sure that you choose "Add Python to environmental variables" during installation.
2. Git - Download and install Git [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Next Steps

1. Change directory to preferred install location
```bash 
cd /where/you/want/this/installed
```

2. Clone DiscoCode

```bash 
git clone https://github.com/nickheyer/DiscoCode
```
 
3. Change directory to DiscoCode
```bash 
cd ./discocode
```

4. Install Requirements
```bash 
pip install -r requirements.txt
```

5. Run Migrations
```bash 
python manage.py migrate
```

6. Run DiscoCode
```bash
sh ./run.sh
```

<hr />
<br />

## Features 🌟

    **Multi-Language Support:** Execute code in a plethora of languages - from mainstream ones like Python, Java, C++, JavaScript, to esoteric ones like Rockstar, Cow, and Lolcode.
    **Containerized Execution:** Ensures safe and isolated code execution environment.
    **Discord Integration:** Directly execute code from Discord with an easy-to-use command system.
    **User Roles and Authorization:** Manage permissions with roles like admin, user, unrestricted, and owner.
    **User Debug Information:** Quickly access user roles and registered commands.

## How to Use 📘
To execute code, use the prefix for code execution ($ by default), followed by three backticks and the language that you would like to code in. Then, on a new line below that, you can start writing code. End it with a new line and another three backticks.

````markdown
  $```python
  print("Hello, DiscoCode!")
  ```
````

## Contributing 💼
Feel free to fork this repository, add your features or improvements and create a pull request. We are excited to see your creative ideas!

## License 📄
This project is licensed under the MIT License - see the LICENSE.md file for details.

Happy Coding! 🚀