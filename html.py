# - #


gpio = 2
ftp = "off"
n = 0

http = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"  # HTTP response

index = """
<html>
    <head> 
        <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="5">
    <link rel="icon" href="data:,">
    
    <style>
        html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        body{background-color: black;}
        h1{color: #0F3376; padding: 2vh;}
        h3{color: #0F3376; padding: 2vh;}
        p{color: white; font-size: 1.2rem;}
        .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{background-color: #4286f4;}
        .button3{background-color: #F286f4;}
        .button4{background-color: #9d2424;}
    </style>""" + f"""
    
    </head>
    <body> 
        <h1>ESP Web Server</h1> 
        <h1></h1>
        <h3>{n}</h3>
        <p>Backlight:  <strong> {gpio} </strong></p>
        <p>FTP Server:  <strong> {ftp} </strong></p>
        <p></p>
        <p><a href="/?led=on">  <button class="button button">ON</button>     </a></p>
        <p><a href="/?led=off"> <button class="button button2">OFF</button>   </a></p>
        <p><a href="/?ftp=on">  <button class="button button3">FTP</button>   </a></p>
        <p><a href="/?reset">   <button class="button button4">RESET</button> </a></p>
    </body>
</html>
"""
