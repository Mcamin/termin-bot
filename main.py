from Behorde.behorde import Auslanderbehorde



def main(v_url):
    """
    Main function call
    :param v_url: the website url
    :return:
    """
    ab = Auslanderbehorde(v_url)
    ab.run()


if __name__ == "__main__":
    main('https://otv.verwalt-berlin.de/ams/TerminBuchen')

