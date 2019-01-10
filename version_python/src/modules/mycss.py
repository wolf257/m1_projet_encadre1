def generate_css(file):
    content = """
    body{
        border: solid 10px black;
        padding: 40px;
        background-color: #fdf6e3;
        font-family: "Comic Sans MS";
        max-width: 900px;
        margin: 20px auto 20px auto;
    }

    h2{
        padding-top: 10 px;
        margin-top: 40px;
        text-align: center;
        text-decoration: underline;
    }


    /* ----------------------
    PARTIE Liens
    ------------------------*/
    a:link{
        color: black;
        padding: 14px 25px;
        text-decoration: underline;
    }

    a:visited {
        color: gray;
    }

    /* ----------------------
    PARTIE Table
    ------------------------*/
    table{
        width:80%;
        margin:auto;
        overflow: hidden;
    }

    tr{
        text-align: center;
    }

    td{
        border: .5px solid brown;
        border-radius: 10px;

    }
    """

    with open(file, mode='w', encoding="utf8") as fileout:
        fileout.write(content)
