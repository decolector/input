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

echo '015A3031024141060A49310A4F310E30303008304573746504'|xxd -r -p | nc 192.168.1.105 9520

echo '015A3030024141061B30621C311A310A49310A4F3162617204'|xxd -r -p | nc 192.168.1.105 9520

echo '015A3030024141061B30621C311A310A49310A4F31666F6F04' | xxd -r -p | > /dev/ttyp0

echo $'\x01\x5A\x30\x30\x02\x41\x41\x06\x1B\x30\x62\x1C\x31\x1A\x31\x0A\x49\x31\x0A\x4F\x31\x62\x61\x72\x04' > /dev/ttyp0

echo $'\x01\x5A\x30\x30\x02\x41\x41\x06\x1B\x30\x62\x1C\x31\x1A\x31\x0A\x49\x31\x0A\x4F\x31\x57\x65\x6C\x63\x6F\x6D\x65\x04' > /dev/ttyp0

'015A3030024141061B30621C311A310A49310A4F3162617204'


Delete line
echo '015A303002455403'| xxd -r -p | nc 192.168.1.100 9520

01 5A 3031 02 45 23 (default values ) 04

echo 015A3031024523C1DEF1MeOeT0W004 | xxd -r -p| 192.168.1.105 9520


# Input specs

    * cola: 20 mensajes
    * tiempo x mensaje: en relacion a la cantidad de caracteres ( 3 rondas )
    * se mueven siempre a la izq
    * autor y mensaje son campos requeridos
    

## Formato del mensaje

lorem impsum (author)
lorem ipsum - att: author

echo '015A3031024141060A49310A4F310E30303008394573746504' | xxd -r -p| nc 192.168.1.105 9520


015A3030024141 06 0A 49314F310E30 686F6C6120616E61 04

015A3031024141060A49314142434404

015A3031024141060A49310A4F310E30303008394573746504

move left pause 3 secs move left
echo '01 5A 3031 02 41 06 0A49310A4F310E00  41 42 43 44 04' | xxd -r -p| nc 192.168.1.105 9520

Simple display text
01 + 5A + 3031 + 02 + 4141 + 06 + 45737465 04

Display text moving left default 3 secs pause
01 + 5A + 3031 + 02 + 4141 + 06 + 0A4931 + 0A4F31 + 45737465 04
015A3031024141060A49310A4F314573746504

Display text moving left no pause
01 + 5A + 3031 + 02 + 4141 + 06 + 0A4931 + 0A4F31 + 0E303030 + 45737465 04
015A3031024141060A49310A4F310E3030304573746504

Display text moving left no pause
01 + 5A + 3031 + 02 + 4141 + 06 + 0A4931 + 0A4F31 + 0E303030 +  + 45737465 04
015A3031024141060A49310A4F310E3030304573746504

Display text moving left no pause line space
01 + 5A + 3031 + 02 + 4141 + 06 + 0A4931 + 0A4F31 + 0E303030 + 0830 + 45737465 04
015A3031024141060A49310A4F310E30303008304573746504

echo '015A3031024141060A49310A4F310E30303008304573746504'|xxd -r -p | nc 192.168.1.105 9520

{
  _id: ObjectId("53472eb56173910002000755"),
  body: "`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_)`'-.,_",
  author: "( '-.( '-.,",
  date: 1397173941303
}