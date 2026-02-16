import fitz

doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), "Hello, this is a test PDF for the converter app!", fontsize=20)
doc.save("test.pdf")
print("test.pdf created")
