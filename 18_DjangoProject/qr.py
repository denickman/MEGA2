import qrcode
# need pillow library to be able to process qr code image

image = qrcode.make('https://127.0.0.1:8000')
image.save('qr.png')


