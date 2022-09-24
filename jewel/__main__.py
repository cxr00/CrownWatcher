from jewel import Jewel, Colony


def main():
    j = Jewel()
    j.refresh()
    c = Colony(j)
    c.defame_crown()
    c.condense()
    c.archive()


if __name__ == "__main__":
    main()
