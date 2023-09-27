# DiscoCode

![image](https://github.com/nickheyer/DiscoCode/assets/60236014/64f05226-3d9f-42e8-b5b5-94465413140f)

### Your friendly neighborhood containerized code execution web server and discord bot.
Safe and secure. Powered by Piston. Includes a REST API for code running, user admin, and database management.


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
docker run -d -p 6565:6565 --name discocode nickheyer/discocode
```
##### The server within the docker container can be accessed locally at [http://127.0.0.1:6565](http://127.0.0.1:6565)

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


## General Instructions


### Accessing The Web-UI

#### *You will need to get the IP address of the computer hosting DiscoCode. On Windows, you would typically type `ipconfig` on the host machine and look for your `ipv4`.*

#### *If you would like to access DiscoCode remotely, as in not on the same network as the host machine, you will need to do some port forwarding to expose port 6565 to the internet. Run into trouble? Feel free to join the [Discord](https://discord.com/invite/6Z9yKTbsrP)!*

<hr />

### Configuration

#### *DiscoCode requires a small amount of configuration before you can begin making requests. Discord Token for example.*

<hr />

#### *To get your Discord Token, go to the "bot" tab in your developer portal. You may need to click "reset Token" and/or enter authentication code if you have 2FA enabled. Make sure to enable all `Privileged Gateway Intents`)*
![Peek 2023-05-22 22-06](https://github.com/nickheyer/DiscoCode/assets/60236014/b197418d-ef70-4a74-9b0d-d43d6802f45b)

#### *If you haven't already, now is also a good time to invite the bot to the server or servers you would like to monitor, you can do that via the Discord Developer Portal. Admin access is the only level we have tested. Anything less may result in errors.*
![Peek 2023-04-07 20-01](https://user-images.githubusercontent.com/60236014/230700480-36a89984-59ea-4c65-a269-1d4e34230872.gif)


<hr />

<br />

## Usage


### Add Yourself As An Admin

In the Web UI, click "Users". Add yourself as a user, but before confirming, change "Non-Admin" to "Admin". Your username should match your Discord username. These are automatically populated in the search bar when the bot is running and can see other users.


### Test That The Bot Is Running

Type the following into a discord chat message that the bot can see:

```
!dc help
```


## Features 🌟

  - *Multi-Language Support:* Execute code in a plethora of languages - from mainstream ones like Python, Java, C++, JavaScript, to esoteric ones like Rockstar, Cow, and Lolcode.

  - *Containerized Execution:* Ensures safe and isolated code execution environment.

  - *Discord Integration:* Directly execute code from Discord with an easy-to-use command system.

  - *User Roles and Authorization:* Manage permissions with roles like admin, user, unrestricted, and owner.
  
  - *User Debug Information:* Quickly access user roles and registered commands.

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
