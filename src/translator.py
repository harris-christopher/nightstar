
class Translator:

    # Step 1 - Create sister file if it doesn't yet exist
    # Step 2 - Scan sister file for untranslated sections
    #  * setup "chunks" of work to be done - involves looking at untranslated file to determine best chunking process
    #  * hint: Go by id, not line number,  to avoid alignment issues if api returns things slightly differently
    # Step 3 - have semaphores process whichever chunks are not currently being processed (can go in ascending order)
    #  * have them update the file in-place
    # TODO: ls shouldn't need to exist - le may or may not need to exist
    # TODO: le could also be FILE to include or stop at
    pass
