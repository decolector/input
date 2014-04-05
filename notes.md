# Network communication

"Welcome" message hex string: '015A3030024141061B30621C311A310A49310A4F3157656C636F6D6504'

netcat line:

echo '015A3030024141061B30621C311A310A49310A4F3157656C636F6D6504'|xxd -r -p | nc 192.168.1.105 9520

'015A3030024141061B30621C311A310A49310A4F31'+ '57656C636F6D65' +'04'

where

'57 65 6C 63 6F 6D 65'
 W  e  l  c  o  m  e

666f6f = foo

626172 = bar

62697a = biz

# Redirect to serial port with socat

sudo socat -d -d -d GOPEN:/dev/ptyp0,ignoreeof tcp:192.168.1.105:9520

echo '015A3030024141061B30621C311A310A49310A4F31666f6f04'|xxd -r -p | nc 192.168.1.105 9520

echo '015A3030024141061B30621C311A310A49310A4F3162617204'|xxd -r -p | nc 192.168.1.105 9520

echo '015A3030024141061B30621C311A310A49310A4F31666F6F04' | xxd -r -p | > /dev/ttyp0

echo $'\x01\x5A\x30\x30\x02\x41\x41\x06\x1B\x30\x62\x1C\x31\x1A\x31\x0A\x49\x31\x0A\x4F\x31\x62\x61\x72\x04' > /dev/ttyp0

echo $'\x01\x5A\x30\x30\x02\x41\x41\x06\x1B\x30\x62\x1C\x31\x1A\x31\x0A\x49\x31\x0A\x4F\x31\x57\x65\x6C\x63\x6F\x6D\x65\x04' > /dev/ttyp0

'015A3030024141061B30621C311A310A49310A4F3162617204'


# Input specs

    * cola: 20 mensajes
    * tiempo x mensaje: en relacion a la cantidad de caracteres ( 3 rondas )
    * se mueven siempre a la izq
    * autor y mensaje son campos requeridos
    

## Formato del mensaje

lorem impsum (author)
lorem ipsum - att: author

