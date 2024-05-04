import requests
# import serial
import time
import maze

BOT_Username = '@TeamUno1bot'

class BotTelegram:
    def __init__(self, serial_port='COM5', baud_rate=9600):
        # self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
        self.lampu_A_status = 'OFF'
        self.lampu_B_status = 'OFF'
        self.last_message_id = None
        self.maze = None  # Initialize the maze object

    def send_telegram_request(self, method, data):
        token = "7181750288:AAEsny_8Yxefryhbe3Z5-FW3qZB4X8AFzK0"
        url = f"https://api.telegram.org/bot{token}/{method}"
        response = requests.post(url, json=data)
        return response.json()

    def delete_message(self, chat_id, message_id):
        self.send_telegram_request("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

    def     start(self, message):
        chat_id = message["chat"]["id"]
        if self.last_message_id:
            self.delete_message(chat_id, self.last_message_id)
        sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Halo, saya adalah Bot dari team 1 MBKM Dago. Academy."})
        self.last_message_id = sent_message["result"]["message_id"]
        time.sleep(0.1)  # Small delay to avoid rate limiting
        sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Pada Bot ini, anda bisa: melakukan command pada robot ArduinoUno kami, mendapatkan informasi mengenai ArduinoUno, dan melakukan Search Problem menggunakan Maze (Labyrinth)"})
        self.last_message_id = sent_message["result"]["message_id"]
        time.sleep(0.1)
        # sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Ini adalah beberapa command yang bisa kamu ketik: \n \n /startUno - Untuk Memulai Command ArduinoUno kami \n /startSearch - Untuk memulai Search Problem Maze kami \n \n Untuk command yang lengkap, tolong ketik symbol ''/'' "})
        # self.last_message_id = sent_message["result"]["message_id"]
        keyboard = self.get_markup_start()
        sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Silahkan pilih command:", "reply_markup": keyboard})
        self.last_message_id = sent_message["result"]["message_id"]

    def get_markup_start(self):
        keyboard = {
            "inline_keyboard": [
                [{"text": "Maze", "callback_data": "maze"}, {"text": "Uno", "callback_data": "menu"}],
                [{"text": "Help", "callback_data": "help"}, {"text": "Custom", "callback_data": "custom"}]
            ]
        }
        return keyboard

    def help_command(self, message):
        chat_id = message["chat"]["id"]
        if self.last_message_id:
            self.delete_message(chat_id, self.last_message_id)
        sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Apakah terjadi kendala pada bot ini? Silahkan untuk melakukan contact pada salah satu Team Kami @Voldemort101010"})
        self.last_message_id = sent_message["result"]["message_id"]

    def custom_command(self, message):
        chat_id = message["chat"]["id"]
        if self.last_message_id:
            self.delete_message(chat_id, self.last_message_id)
        sent_message = self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Ini adalah command custom"})
        self.last_message_id = sent_message["result"]["message_id"]

    def menu_maze(self, message):
        chat_id = message["chat"]["id"]
        keyboard = self.get_markup_maze()
        self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Pilih Opsi Menu Berikut:", "reply_markup": keyboard})

    def get_markup_maze(self):
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "Generate Maze", "callback_data": "generate_maze"},
                    {"text": "Solve Maze", "callback_data": "solve_maze"}
                ]
            ]
        }
        return keyboard

    def menu_bot(self, message):
        chat_id = message["chat"]["id"]
        keyboard = self.get_markup_bot()
        self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": "Pilih Opsi Menu Berikut:", "reply_markup": keyboard})

    def get_markup_bot(self):
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": f'Lampu A : {self.lampu_A_status}', "callback_data": "lampu_A"},
                    {"text": f'Lampu B : {self.lampu_B_status}', "callback_data": "lampu_B"}
                ],
                [
                    {"text": "Baca Sensor Jarak", "callback_data": "Read_J"},
                    {"text": "Baca Sensor Suhu", "callback_data": "Read_S"}
                ]
            ]
        }
        return keyboard

    def handle_button_click(self, callback_query):
        button_data = callback_query["data"]
        message = callback_query["message"]
        message_id = message["message_id"]
        chat_id = message["chat"]["id"]

        if button_data == "lampu_A":
            if self.lampu_A_status == 'OFF':
                # self.ser.write(b'R1 ON\n')
                self.lampu_A_status = 'ON'
            else:
                # self.ser.write(b'R1 OFF\n')
                self.lampu_A_status = 'OFF'
        elif button_data == "lampu_B":
            if self.lampu_B_status == 'OFF':
                # self.ser.write(b'R2 ON\n')
                self.lampu_B_status = 'ON'
            else:
                # self.ser.write(b'R2 OFF\n')
                self.lampu_B_status = 'OFF'
        elif button_data == "Read_J":
            # self.ser.write(b'RU\n')
            # time.sleep(1)
            # self.ser.flushInput()
            # response = self.ser.readline().decode().strip()
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
        elif button_data == "Read_S":
            # self.ser.write(b'RS\n')
            # time.sleep(1)
            # self.ser.flushInput()
            # response = self.ser.readline().decode().strip()
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
        elif button_data == "generate_maze":
            # Generate random maze
            random_maze = maze.generate_maze()
            maze_text = maze.generate_maze_text(random_maze)
            self.maze = random_maze
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": maze_text})
        elif button_data == "solve_maze":
            if self.maze is not None:
                awal = (0, 0)
                akhir = (maze.UKURAN[0] - 1, maze.UKURAN[1] - 1)
                solusi = maze.bfs(self.maze, awal, akhir)
                if solusi is None:
                    self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": f"Maze tidak dapat diselesaikan"})
                else:
                    teks = "Langkah untuk menyelesaikan maze:\n"
                    for i, step in enumerate(solusi):
                        teks += f"{i+1}. {step}\n"
                    self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": teks})
            else:
                response = "Maze belum dibuat. Silakan gunakan opsi 'Generate Maze' terlebih dahulu."
                self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response})
        elif button_data == "maze":
            self.menu_maze(message)
        elif button_data == "menu":
            self.menu_bot(message)
        elif button_data == "custom":
            self.custom_command(message)
        elif button_data == "help":
            self.help_command(message)

    def process_message(self, message):
        if not message or 'chat' not in message or 'id' not in message['chat']:
            print("Invalid message format or missing chat ID.")
            return

        text = message.get("text", "").lower()  # Convert text to lowercase
        chat_id = message["chat"]["id"]
        message_type = message.get("chat", {}).get("type", "")

        print(f'User ({chat_id}) in {message_type}: "{text}" ')

        # Massage Handler(Chat)
        if "halo" in text:  # Checking for "halo" regardless of capitalization
            response_text = "Hai selamat datang!"
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response_text})
            return
        elif "apa yang dimaksud arduino" in text:
            response_text = "Arduino adalah platform sumber terbuka untuk membangun proyek elektronika yang interaktif dengan papan mikrokontroler dan perangkat lunak pengembangan terintegrasi."
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response_text})
            return
        elif "apa itu arduino uno" in text:
            response_text = "Arduino Uno adalah papan mikrokontroler yang sangat populer dan serbaguna yang merupakan bagian dari keluarga produk Arduino. Ini memiliki sejumlah pin input/output digital dan analog yang dapat digunakan untuk mengendalikan berbagai perangkat dan sensor elektronik. Uno hadir dengan prosesor ATmega328P dan memiliki antarmuka USB yang memungkinkan untuk pemrograman dan komunikasi dengan komputer."
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response_text})
            return
        elif "bagaimana cara kerja arduino uno" in text:
            response_text = "Berikut langkah-langkah umum untuk menggunakan Arduino Uno: \nPersiapan Perangkat: Sambungkan Arduino Uno ke komputer menggunakan kabel USB yang disertakan. Pastikan Anda memiliki IDE Arduino terinstal di komputer Anda.\nIDE Arduino: Buka Arduino IDE. IDE ini menyediakan lingkungan untuk menulis, menguji, dan mengunggah kode ke Arduino Uno.\nMenulis Kode: Tulis program Arduino menggunakan bahasa pemrograman C/C++. Gunakan fungsi-fungsi dan library yang tersedia untuk mengendalikan komponen elektronika yang terhubung ke Arduino.\nPemrograman: Setelah menulis kode, verifikasi kode dengan memilih 'Verify/Compile' (Ctrl + R). Pastikan tidak ada kesalahan sintaks dalam kode.\nMemilih Board dan Port: Pilih jenis board Arduino yang digunakan (Arduino Uno) dari menu 'Tools' > 'Board'. Kemudian, pilih port serial yang sesuai dari menu 'Tools' > 'Port'.\nMengunggah Kode: Tekan tombol 'Upload' (Ctrl + U) untuk mengunggah kode ke Arduino Uno. Proses ini akan mengkompilasi dan memuat program ke papan Arduino.\nPemantauan Serial (Opsional): Jika program Anda menggunakan output serial, Anda dapat memantau outputnya menggunakan 'Serial Monitor' dari menu 'Tools'.\nKoneksi Perangkat: Sambungkan komponen atau perangkat elektronika lainnya ke pin input/output digital atau analog Arduino Uno sesuai dengan kebutuhan proyek Anda.\nMenjalankan Program: Setelah mengunggah kode ke Arduino Uno dan menghubungkan perangkat, Anda dapat menjalankan program dengan menyalakan Arduino Uno. Program Anda sekarang akan berjalan di Arduino Uno dan mengendalikan perangkat yang terhubung."
            self.send_telegram_request("sendMessage", {"chat_id": chat_id, "text": response_text})
            return

        # Massage Handler (/command)
        if "/start" in text:
            self.start(message)
        elif "/Menu" in text:
            self.menu_bot(message)
        elif "/Maze" in text:
            self.menu_maze(message)
        elif "/Help" in text:
            self.help_command(message)
        elif "/Custom" in text:
            self.custom_command(message)

if __name__ == '__main__':
    bot_telegram = BotTelegram()

    print('Polling...')
    offset = 0
    while True:
        try:
            response = bot_telegram.send_telegram_request("getUpdates", {"offset": offset, "timeout": 30})
            if response["ok"]:
                for result in response["result"]:
                    bot_telegram.process_message(result.get("message", {}))
                    if "callback_query" in result:
                        bot_telegram.handle_button_click(result["callback_query"])
                    offset = result["update_id"] + 1
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred:", e)
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            break
        except Exception as e:
            print("An unexpected error occurred:", e)
            break
