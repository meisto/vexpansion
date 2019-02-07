import re # Regexp
import sys
import os
import socket

import vim

# -----------------------------------------
# -- Util ---------------------------------
# -----------------------------------------

# Returns a string to be used as prefix for indentations
def tab_prefix():
    # Find number of prefixed tabs on the current line
    current_line = vim.current.line
    prefix = re.search("^\t*", current_line).group(0)
    # Get only the first element if more than one fit is found
    prefix = prefix if (type(prefix)) == str else prefix[0]
    return prefix;


# Insert a custom html tag after the current line, where the tag name is given
# It is possible to enter full strings with class information.
# Example: "a class='foo' id='bar'" will yield the tag 
# <a class='foo' id='bar'> ... </a> with indention
def html_tag(tag_name, indent):
    indent = int(indent)

    # Remove any class, id, etc inforamtions on the closing tag
    close_tag_name = tag_name.split(" ")[0]
    
    # You can modify this code to change the resulting tag
    prefix = tab_prefix() + "\t" * indent
    tag_open = prefix + "<" + tag_name + ">\n"
    tag_content = prefix + "\t\n"
    tag_close = prefix+ "</" + close_tag_name + ">\n"
    tag_str = tag_open + tag_content + tag_close

    # write tags in the vim buffer
    vim_range = vim.current.range
    vim_range.append(tag_open)
    vim_range.append(tag_content)
    vim_range.append(tag_close)
    return

# Write content of a file in the vim buffer starting from the active line
# The file to be inserted is specified by a url
def insert_file(file_name):
    (current_row, _) = vim.current.window.cursor
    buf = vim.current.buffer

    # Open file, get a list of its content and write it into the vim buffer
    f = open("vexpansion/" + file_name, mode='r')
    f = f.readlines()
    buf[current_row-1:current_row-1] = f
    return

# -----------------------------------------
# -- Auto-complete ------------------------
# -----------------------------------------
def startOfWord():
    line = vim.current.line
    (_, column) = vim.current.window.cursor

    while(column > 0 and line[column - 1] != ' '):
        column -=1

    if (column <= 0):
        column = 0
    
    vim.command("let result = " + str(column)) # Store result in a VimScript variable
    return

def start_server():
    os.system("java -jar vexpansion/server/Vim_Autocomplete.jar &")
    return

def getSuggestion(prefix):
    # Fun fact for this function: You will see some commented vim.command("echoerr '....'") lines. This is because echoerr not only 
    # prints to sys.stderr or the equivalent. It also raises an error which is almost impossible to track because of the mess it creates.
    # Because of this, error messages will be printed witch echo and an '[ERROR]:' prefix
    # Also some lines of output are not shown, because they are overwritten too fast. This is a problem with the vim configuration.

    # Set up local socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 2010))

    # Protokoll
    def contactServer():
        s.settimeout(3)

        i = 1
        while i < 6:
            try:
                s.sendto(bytes(prefix, "utf-8"), ("127.0.0.1", 2000))
                data, address = s.recvfrom(1024)
                vim.command("let x = " + str(data, "utf-8"))
                return True
            except:   
                errortext = str(sys.exc_info()[0]).replace('\'', '').replace('\"', '')
                vim.command("echom '[ERROR]: Server timout (" + str(i) + "/5) " + errortext + "'")
            i += 1
        vim.command("sleep 3000m")
        vim.command("let x = [\"\"]")
        return False

    try:
        # tests whether the server can be contacted and prints out whether a message was delivered
        hadContact = contactServer()
        if not hadContact:
            vim.command("echom '[ERROR]: Server is offline, try restarting it.'")
            vim.command("sleep 3000m")
    
    except:
        vim.command("echom '[ERROR]: Something went wrong:" + str(sys.exc_info()[0]) + "'")
        vim.command("let x = []")
    
    s.close()
