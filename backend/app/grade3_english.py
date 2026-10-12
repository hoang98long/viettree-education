"""Short, original grade-three English contexts and communication preparation."""

from app.grade3_support import unit

ENGLISH = [
    unit(
        "self",
        "greetings",
        "Hello! Chào hỏi và giới thiệu tên",
        "Dùng Hello hoặc Hi để chào. Hỏi tên: What is your name? Trả lời: My name is... Thực hành nói cùng người hướng dẫn, không chỉ đọc thầm.",
        "Hello! My name is Mai. What is your name? My name is Ben. Nice to meet you, Ben. Nice to meet you, Mai. Đây là cuộc gặp đầu tiên của hai bạn.",
        "Dùng your khi hỏi người đối diện và my khi giới thiệu mình.",
        "Tìm câu chào, câu hỏi tên và câu trả lời.|Đối chiếu người hỏi, người đáp để chọn my hoặc your.|Đọc theo cặp rồi đổi vai để kiểm tra cách dùng.",
        """Câu nào dùng để chào?|Hello!|Goodbye!|Stand up!|Hello là lời chào.
Câu nào hỏi tên?|What is your name?|How old are you?|Where is the pen?|What is your name hỏi tên người đối diện.
Điền từ: ... name is Mai. (Điền từ chỉ 'của tôi'.)|My|Your|His|My name is dùng để tự giới thiệu tên.
Trong đoạn mẫu, Mai gặp ai?|Ben|Tom|Lucy|Cuộc hội thoại nêu Mai và Ben.""",
    ),
    unit(
        "self",
        "age",
        "How old are you? Hỏi và nói tuổi",
        "Hỏi tuổi bằng How old are you? Trả lời I am eight hoặc I am eight years old. Học các số từ 1 đến 10 và dùng đúng thông tin của mình.",
        "My name is Nam. I am nine years old. My friend is Hoa. She is eight years old. We are friends. We say hello at school and play together after class.",
        "Tên và tuổi là hai loại thông tin khác nhau.",
        "Xem câu hỏi cần tên hay tuổi.|Tìm số đi cùng years old để nhận ra tuổi.|Đọc lại câu đầy đủ, giữ đúng người được hỏi.",
        """Theo đoạn mẫu, Nam bao nhiêu tuổi?|Nine|Eight|Seven|Nam nói I am nine years old.
Hoa bao nhiêu tuổi?|Eight|Nine|Ten|Đoạn viết She is eight years old về Hoa.
Câu nào hỏi tuổi?|How old are you?|What is your name?|What colour is it?|How old hỏi tuổi.
Điền từ: I ... nine years old. (Dạng của be đi với I.)|am|is|are|I đi với am.""",
    ),
    unit(
        "school",
        "supplies",
        "Đồ dùng học tập: a pen, a book",
        "Dùng This is a... để giới thiệu một vật ở gần. A pen là một bút mực, a pencil là một bút chì, a ruler là một thước.",
        "This is my bag. There is a book in it. This is a pen. It is blue. I have a ruler, too. I put my school things in the bag after class.",
        "Danh từ số ít thường có a hoặc an trong mẫu câu giới thiệu.",
        "Tìm từ chỉ đồ dùng trong câu.|Quan sát số ít và vị trí vật được nhắc đến.|Đọc lại mẫu This is a... với từng đồ dùng.",
        """Từ nào có nghĩa là 'thước kẻ'?|Ruler|Cat|Mother|Ruler là thước kẻ.
Trong đoạn mẫu, chiếc bút có màu gì?|Blue|Red|Green|Câu It is blue nói về pen.
Câu nào giới thiệu một quyển sách?|This is a book.|This is books.|I am a book.|This is a book giới thiệu một vật.
Điền từ: This is a ... . (Điền từ tiếng Anh nghĩa là 'bút mực'.)|pen|cat|dog|Pen nghĩa là bút mực.""",
    ),
    unit(
        "school",
        "classroom",
        "Chỉ dẫn đơn giản trong lớp học",
        "Stand up là đứng lên, sit down là ngồi xuống, open your book là mở sách. Please làm lời yêu cầu lịch sự hơn.",
        "Teacher: Stand up, please. Children: Good morning! Teacher: Sit down, please. Open your books. Ben opens his book and looks at the picture. Các em thực hành với động tác an toàn.",
        "Nghe người hướng dẫn đọc chậm và làm đúng động tác để luyện nghe thật.",
        "Tìm động từ ở đầu chỉ dẫn.|Ghép stand up, sit down, open với động tác phù hợp.|Nhờ người hướng dẫn đổi thứ tự chỉ dẫn để kiểm tra em hiểu.",
        """Stand up yêu cầu làm gì?|Đứng lên|Ngồi xuống|Đóng sách|Stand up là đứng lên.
Sit down yêu cầu làm gì?|Ngồi xuống|Chạy ra ngoài|Vẽ tranh|Sit down là ngồi xuống.
Từ nào giúp yêu cầu lịch sự hơn?|Please|Cat|Blue|Please được dùng trong lời yêu cầu lịch sự.
Open your book yêu cầu làm gì?|Mở sách|Cất bút|Đóng cửa|Open your book là mở sách.""",
    ),
    unit(
        "family",
        "members",
        "Gia đình: mother, father, sister",
        "Học từ gọi người thân: mother, father, brother, sister. Dùng This is my... để giới thiệu. Không suy đoán thành viên gia đình từ hình mẫu.",
        "This is my family. This is my mother. Her name is Linh. This is my father. His name is Minh. My sister is An. We read books together in the living room.",
        "He và his dùng trong ví dụ nói về bố; she và her nói về mẹ hoặc chị, em gái.",
        "Tìm từ gọi quan hệ trong gia đình.|Đối chiếu tên với mother, father hoặc sister ở câu trước.|Đọc lại cả câu, không chọn chỉ vì tên quen thuộc.",
        """Trong đoạn mẫu, mẹ tên gì?|Linh|Minh|An|Her name is Linh nói về mother.
Bố tên gì?|Minh|Linh|An|His name is Minh nói về father.
Từ nào có nghĩa là 'chị hoặc em gái'?|Sister|Brother|Father|Sister chỉ chị hoặc em gái.
Điền từ: This is my ... . (Điền từ nghĩa là 'mẹ'.)|mother|father|brother|Mother nghĩa là mẹ.""",
    ),
    unit(
        "family",
        "pronouns",
        "He, she và tên người thân",
        "He và she giúp nhắc lại người đã giới thiệu. He is... và she is... đi với is. Chú ý câu trước để biết đại từ chỉ ai.",
        "This is my brother. He is ten. This is my sister. She is seven. My brother has a blue bag. My sister has a red book. They are in the living room.",
        "Không dùng am sau he hoặc she trong mẫu câu này.",
        "Tìm người được giới thiệu trước đại từ.|Ghép he với brother, she với sister trong đoạn mẫu.|Đọc câu liền trước để kiểm tra đại từ chỉ đúng người.",
        """Trong đoạn mẫu, brother bao nhiêu tuổi?|Ten|Seven|Nine|He is ten nói về brother.
Sister bao nhiêu tuổi?|Seven|Ten|Eight|She is seven nói về sister.
Điền từ: She ... seven. (Dạng của be đi với she.)|is|am|are|She đi với is.
Trong đoạn mẫu, ai có túi xanh?|Brother|Sister|Mother|My brother has a blue bag.""",
    ),
    unit(
        "home",
        "rooms",
        "Các phòng trong nhà",
        "Bedroom là phòng ngủ, kitchen là bếp, living room là phòng khách. Hỏi vị trí: Where is...? Trả lời It is in... với đồ vật.",
        "This is my home. The bed is in the bedroom. The table is in the kitchen. My book is in the living room. I keep my rooms clean and put my toys away.",
        "Thông tin về nhà trong bài là ví dụ, không cần chia sẻ địa chỉ thật.",
        "Tìm tên đồ vật câu hỏi nhắc đến.|Đọc cụm in the... để nhận ra phòng.|Kiểm tra không đổi thông tin giữa các đồ vật.",
        """Theo đoạn mẫu, giường ở phòng nào?|Bedroom|Kitchen|Living room|The bed is in the bedroom.
Bàn ở phòng nào?|Kitchen|Bedroom|Garden|The table is in the kitchen.
Từ nào có nghĩa là 'phòng khách'?|Living room|Bedroom|Kitchen|Living room là phòng khách.
Câu nào hỏi vị trí chiếc sách?|Where is the book?|How old is the book?|What is your name?|Where hỏi vị trí.""",
    ),
    unit(
        "home",
        "positions",
        "In, on, under: vị trí đồ vật",
        "In là ở trong, on là ở trên bề mặt, under là ở dưới. Dùng đồ vật an toàn để thực hành đặt và nói vị trí.",
        "The ball is under the table. The book is on the desk. The pen is in the bag. Mai looks for her pen. She opens the bag and finds it there.",
        "Đọc đúng đồ vật, nơi và giới từ của từng câu.",
        "Khoanh tên đồ vật cần tìm.|Tìm in, on hoặc under trong câu tương ứng.|Đặt thử một vật rồi nói lại để phân biệt ba vị trí.",
        """Theo đoạn mẫu, quả bóng ở đâu?|Under the table|On the table|In the bag|Câu đầu nêu ball under the table.
Quyển sách ở đâu?|On the desk|Under the desk|In the bag|The book is on the desk.
Điền từ: The pen is ... the bag. (Theo đoạn mẫu.)|in|under|on|Đoạn mẫu đặt pen in the bag.
Mai tìm được bút ở đâu?|Trong túi|Trên bàn|Dưới ghế|She opens the bag and finds it there.""",
    ),
    unit(
        "toys",
        "toys",
        "Đồ chơi và số lượng đơn giản",
        "A kite là một diều, a doll là một búp bê, a car là một ô tô đồ chơi. There is đi với một vật; there are đi với nhiều vật.",
        "I have a toy box. There is a kite in the box. There are two cars, too. My doll is on the chair. I put my toys away when I finish playing.",
        "Nhiều danh từ số nhiều thêm s; chú ý số lượng trước danh từ.",
        "Tìm tên đồ chơi và số lượng.|Một vật dùng is, nhiều vật dùng are trong mẫu there.|Đọc lại cả câu để kiểm tra danh từ số ít hay số nhiều.",
        """Theo đoạn mẫu, có mấy ô tô đồ chơi?|Two|One|Three|There are two cars.
Từ nào có nghĩa là 'diều'?|Kite|Chair|Book|Kite là diều.
Búp bê trong đoạn mẫu ở đâu?|On the chair|In the bag|Under the bed|My doll is on the chair.
Điền từ: There ... two cars. (Dạng của be.)|are|is|am|There are dùng với nhiều đồ vật.
Câu nào nói có một con diều?|There is a kite.|There are a kite.|I am a kite.|There is đi với a kite số ít.
Sau khi chơi, em nên làm gì theo đoạn?|Cất đồ chơi|Bỏ ở lối đi|Ném đồ chơi|Put my toys away là cất đồ chơi.""",
    ),
    unit(
        "toys",
        "colours",
        "Màu sắc và hỏi What colour...?",
        "Hỏi màu một vật: What colour is it? Trả lời It is red hoặc It is blue. Học red, blue, green, yellow, white, black qua vật thật.",
        "My kite is yellow. My toy car is red. My ball is blue. I play with the ball in the garden. Then I put the blue ball in my box next to the yellow kite.",
        "Colour dùng trong bản viết Anh Anh; color cũng là cách viết tiếng Anh hợp lệ.",
        "Tìm đồ vật đang được hỏi màu.|Ghép từng đồ vật với từ màu trong chính câu của nó.|Đọc lại đoạn để tránh dùng màu của vật khác.",
        """Trong đoạn mẫu, diều màu gì?|Yellow|Red|Blue|My kite is yellow.
Ô tô đồ chơi màu gì?|Red|Blue|Green|My toy car is red.
Quả bóng màu gì?|Blue|Black|White|My ball is blue.
Câu nào hỏi màu sắc?|What colour is it?|How old are you?|Where is Mai?|What colour hỏi màu.
Từ nào nghĩa là màu xanh lá?|Green|Yellow|White|Green là xanh lá.
Điền từ: It is ... . (Điền từ tiếng Anh nghĩa là 'màu đỏ'.)|red|blue|black|Red nghĩa là đỏ.""",
    ),
    unit(
        "pets",
        "pet-words",
        "Các con vật nuôi quanh em",
        "Cat, dog, fish, bird là những từ chỉ con vật quen thuộc. Dùng I have a... để nói về một con vật trong ví dụ, hoặc I do not have a... khi không có.",
        "Mai has a cat. The cat is white. Ben has a dog. The dog is black. They give their pets water. Mai and Ben do not touch an animal they do not know.",
        "Không tự lại gần con vật lạ; người lớn hướng dẫn việc chăm sóc.",
        "Tìm tên con vật của từng bạn.|Đối chiếu màu với câu ngay sau con vật.|Đọc lại cả đoạn để giữ đúng thông tin của mỗi bạn.",
        """Mai có con vật nào trong đoạn mẫu?|Cat|Dog|Bird|Mai has a cat.
Mèo của Mai màu gì?|White|Black|Blue|The cat is white.
Ben có con vật nào?|Dog|Fish|Cat|Ben has a dog.
Chó của Ben màu gì?|Black|White|Green|The dog is black.
Từ nào có nghĩa là 'chim'?|Bird|Book|Ball|Bird nghĩa là chim.
Theo đoạn, hai bạn cho con vật thứ gì?|Water|Paint|Glue|They give their pets water.""",
    ),
    unit(
        "hobbies",
        "likes",
        "I like... Nói sở thích đơn giản",
        "Dùng I like... để nói điều mình thích. Do you like...? hỏi sở thích; trả lời Yes, I do hoặc No, I do not.",
        "I am Hoa. I like drawing. My friend Nam likes reading. We play in the garden after school. I draw a flower. Nam reads a book about a cat. We show our work to each other.",
        "Câu trả lời cần đúng sở thích trong bài, không chọn theo sở thích riêng của em.",
        "Tìm từ like hoặc likes.|Xem ai là người có sở thích đó.|Ghép câu hỏi Do you like với câu đáp Yes, I do hoặc No, I do not.",
        """Hoa thích hoạt động nào?|Drawing|Reading|Swimming|Hoa nói I like drawing.
Nam thích hoạt động nào?|Reading|Drawing|Singing|My friend Nam likes reading.
Hoa vẽ gì?|A flower|A dog|A car|I draw a flower.
Nam đọc sách về con gì?|A cat|A bird|A fish|Nam reads a book about a cat.
Câu nào hỏi sở thích?|Do you like drawing?|Where is the bag?|How old is Hoa?|Do you like hỏi điều thích.
Điền từ: Yes, I ... . (Trả lời Do you like reading?)|do|am|is|Yes, I do là câu đáp khẳng định.""",
    ),
    unit(
        "hobbies",
        "can",
        "Can: những việc em có thể làm",
        "I can sing nói em có thể hát. I cannot swim nói em không thể bơi. Can you...? là câu hỏi khả năng; luyện nói với hoạt động an toàn.",
        "My name is An. I can sing and draw. I cannot swim. My friend Ben can swim. He cannot sing. We help each other practise, and we always swim with a trusted adult.",
        "Sau can và cannot dùng động từ như sing, draw, swim trong mẫu này.",
        "Tìm can và cannot của từng người.|Tách việc làm được và chưa làm được.|Kiểm tra câu trả lời không bỏ từ phủ định cannot.",
        """Theo đoạn mẫu, An làm được việc nào?|Sing|Swim|Drive|An nói I can sing and draw.
An chưa làm được việc nào?|Swim|Draw|Sing|I cannot swim nói về An.
Ben làm được việc nào?|Swim|Sing|Fly|My friend Ben can swim.
Ben chưa làm được việc nào?|Sing|Swim|Read, theo đoạn|He cannot sing nói về Ben.
Câu nào hỏi khả năng hát?|Can you sing?|What is your name?|Where is your bag?|Can you sing hỏi có thể hát không.
Điền từ: I ... draw. (Điền từ chỉ 'có thể'.)|can|cannot|am|Can biểu thị có thể.""",
    ),
    unit(
        "self",
        "friend-cards",
        "Đọc thẻ bạn nhỏ và nối thông tin",
        "So sánh các thẻ giới thiệu để tìm đúng tên, tuổi và sở thích. Chỉ dùng thông tin trên thẻ; không đoán từ tên.",
        "Mai: I am eight. I like drawing. Ben: I am nine. I like reading. Lucy: I am eight. I like singing. Ba thẻ giúp em luyện tìm thông tin và đặt câu hỏi cho bạn.",
        "Hai bạn có thể cùng tuổi nhưng khác sở thích.",
        "Lập ba hàng cho ba tên.|Ghi tuổi và sở thích vào hai cột riêng.|Kiểm tra tất cả điều kiện câu hỏi, đừng chỉ xét tuổi.",
        """Bạn nào chín tuổi theo các thẻ?|Ben|Mai|Lucy|Ben nói I am nine.
Bạn nào thích vẽ?|Mai|Ben|Lucy|Mai nói I like drawing.
Bạn nào thích hát?|Lucy|Ben|Mai|Lucy nói I like singing.
Mai và Lucy giống nhau ở điều nào?|Tuổi|Sở thích|Tên|Cả hai đều eight, nhưng khác sở thích.
Ben thích hoạt động nào?|Reading|Drawing|Singing|Thẻ Ben ghi I like reading.
Bạn tám tuổi và thích hát là ai?|Lucy|Mai|Ben|Chỉ Lucy đáp ứng đồng thời hai điều kiện.
MULTI|Chọn các bạn tám tuổi theo thẻ.|Mai~Ben~Lucy~Tom|0~2|Mai và Lucy đều ghi eight; không có thẻ Tom.
Câu nào hỏi tuổi của một bạn?|How old are you?|What colour is it?|Where is it?|How old hỏi tuổi.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "school",
        "polite-help",
        "May I...? Xin phép và nhờ giúp",
        "May I come in? xin phép vào. May I borrow your ruler? xin mượn thước. Thank you thể hiện cảm ơn; Excuse me mở lời lịch sự.",
        "Ben: Excuse me. May I borrow your ruler? Mai: Yes. Here you are. Ben: Thank you. Mai: You are welcome. Ben uses the ruler, then gives it back to Mai after class.",
        "Mượn đồ cần được đồng ý và trả lại sau khi dùng.",
        "Tìm người mượn, vật mượn và người cho mượn.|Nhận ra lượt xin phép, đồng ý, cảm ơn, đáp lời.|Đọc theo cặp và kiểm tra cách mở lời lịch sự.",
        """Trong hội thoại, Ben muốn mượn gì?|Ruler|Book|Ball|Ben hỏi borrow your ruler.
Ai cho Ben mượn?|Mai|Lucy|Nam|Mai trả lời Yes. Here you are.
Câu nào dùng để xin phép vào?|May I come in?|I am eight.|It is blue.|May I come in là lời xin phép.
Sau khi nhận thước, Ben nói gì?|Thank you.|Stand up.|Goodbye forever.|Ben cảm ơn khi được giúp.
Câu nào đáp lời cảm ơn?|You are welcome.|How old are you?|Sit down.|You are welcome là cách đáp lời cảm ơn.
Ben làm gì sau khi dùng thước?|Trả lại Mai|Giấu đi|Vứt đi|Đoạn viết gives it back to Mai.""",
        vip=True,
    ),
    unit(
        "home",
        "room-reading",
        "Đọc căn phòng: tìm đúng đồ vật",
        "Ghép đồ vật với vị trí, màu và số lượng. Khi câu hỏi có hai điều kiện, kiểm tra cả hai trước khi chọn.",
        "There are two books on the desk. A red ball is under the chair. A blue pen is in the bag. There is a cat on the bed. Mai puts a ruler next to the books.",
        "In, on và under không thay thế cho nhau.",
        "Tạo một hàng cho từng đồ vật.|Ghi vị trí và đặc điểm vào các cột.|Đọc lại câu gốc khi có hai vật cùng chỗ hoặc gần nhau.",
        """Có bao nhiêu sách trên bàn?|Two|One|Three|There are two books on the desk.
Vật nào ở dưới ghế?|Red ball|Blue pen|Cat|A red ball is under the chair.
Bút xanh ở đâu?|In the bag|On the bed|Under the chair|A blue pen is in the bag.
Con mèo ở đâu?|On the bed|In the bag|Under the desk|There is a cat on the bed.
Thước được đặt cạnh vật gì?|Books|Ball|Cat|Mai puts a ruler next to the books.
Điền từ: The ball is ... the chair. (Theo đoạn.)|under|in|on|Vị trí bóng trong đoạn là under the chair.
Câu nào mô tả bút đúng theo đoạn?|The pen is blue.|The pen is red.|The pen is on the bed.|Đoạn nêu a blue pen.
Vật nào ở trên bàn theo câu đầu?|Books|Cat|Ball|Câu đầu đặt books on the desk.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "toys",
        "lost-toy",
        "Đố mẹo: tìm đồ chơi thất lạc",
        "Dùng các điều kiện phủ định và màu để loại trừ. Bài có ba đồ chơi khác nhau; không tự thêm đồ chơi mới.",
        "There are three toys: a red car, a blue ball and a yellow kite. Ben wants the blue toy. Mai wants the toy that can fly. An takes the toy left. Each child takes one toy.",
        "Toy that can fly ở đây nói về diều trong ba đồ chơi đã liệt kê.",
        "Liệt kê đồ chơi và màu.|Điền điều đã biết: blue và can fly.|Kiểm tra mỗi bạn một đồ chơi, không dùng một món cho hai bạn.",
        """Đồ chơi màu xanh là gì?|Ball|Car|Kite|Đoạn liệt kê a blue ball.
Ben chọn đồ chơi nào?|Ball|Car|Kite|Ben wants the blue toy, tức blue ball.
Mai chọn đồ chơi nào?|Kite|Ball|Car|Trong ba món, diều là toy that can fly.
An chọn đồ chơi nào?|Car|Ball|Kite|Ball thuộc Ben, kite thuộc Mai, còn car.
Ô tô đồ chơi màu gì?|Red|Blue|Yellow|Danh sách nêu a red car.
Diều màu gì?|Yellow|Red|Blue|Danh sách nêu a yellow kite.
MULTI|Chọn hai điều kiện đã cho trong đoạn.|Ben wants the blue toy.~Each child takes one toy.~An wants the blue toy.~There are four toys.|0~1|Hai điều đầu được ghi rõ; An không được gán màu xanh.
Nếu không có điều kiện về Mai, biết chắc Mai chọn gì không?|No, not enough information.|Yes, the car only.|Yes, the ball only.|Khi Ben có ball, Mai có thể chọn car hoặc kite nếu thiếu điều kiện.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "pets",
        "pet-cards",
        "Đọc thẻ con vật và chọn bằng chứng",
        "Đọc các câu ngắn về con vật, tìm chi tiết được nêu rõ. Từ not hoặc cannot thay đổi nghĩa; không bỏ chúng khi trả lời.",
        "Lily has a white cat. It is on the chair. Tom has a black dog. It is under the table. A bird is in a big cage. The bird can sing. The cat cannot fly.",
        "Thông tin về vị trí và khả năng cần đọc ở đúng câu.",
        "Tìm tên và màu con vật.|Gạch chân giới từ hoặc can, cannot liên quan câu hỏi.|Chỉ ra câu chứng minh lựa chọn; không suy đoán điều chưa nêu.",
        """Lily có con vật nào?|White cat|Black dog|Bird|Lily has a white cat.
Mèo ở đâu?|On the chair|Under the table|In the cage|It is on the chair nói về cat.
Tom có con vật nào?|Black dog|White cat|Fish|Tom has a black dog.
Chó ở đâu?|Under the table|On the chair|In the cage|It is under the table nói về dog.
Con vật nào có thể hát theo đoạn?|Bird|Dog|Cat|The bird can sing.
Điền từ: The cat ... fly. (Theo đoạn, điền từ chỉ 'không thể'.)|cannot|can|is|Câu cuối viết cannot fly.
Lồng chim được tả như thế nào?|Big|Small|Red|Đoạn ghi a big cage.
Điều nào chưa được đoạn cho biết?|Tên của con chó|Màu của con mèo|Vị trí con chim|Không có tên chó trong đoạn, chỉ có tên người nuôi Tom.""",
        vip=True,
        thinking=True,
    ),
    unit(
        "hobbies",
        "actions-now",
        "What are you doing? Hoạt động đang diễn ra",
        "Dùng I am reading để nói việc đang làm. He is drawing, she is singing, they are playing là các mẫu hiện tại tiếp diễn đơn giản.",
        "It is a quiet afternoon. I am reading. My sister is drawing a flower. My brother is playing with a ball in the garden. We are at home. My mother is looking at our pictures.",
        "Dùng am, is hoặc are rồi động từ có ing trong mẫu này.",
        "Tìm người thực hiện từng việc.|Ghép I với am, he hoặc she với is.|Đọc cả cụm để nhận ra hoạt động đang diễn ra, không đổi người làm.",
        """Người kể đang làm gì?|Reading|Swimming|Singing|I am reading nói về người kể.
Chị hoặc em gái đang làm gì?|Drawing a flower|Playing with a ball|Reading|My sister is drawing a flower.
Anh hoặc em trai đang ở đâu?|In the garden|At school|In the kitchen|My brother is playing in the garden.
Điền từ: I ... reading. (Dạng của be.)|am|is|are|I đi với am.
Câu nào nói cô ấy đang hát?|She is singing.|She am singing.|She singing is.|She is singing đúng mẫu hiện tại tiếp diễn.
Câu nào hỏi hoạt động đang làm?|What are you doing?|How old are you?|What colour is it?|What are you doing hỏi đang làm gì.""",
        vip=True,
    ),
    unit(
        "family",
        "mixed-review",
        "Kết hợp thông tin về gia đình và sở thích",
        "Bài ngắn kết hợp người, tuổi, sở thích và vị trí. Lập bảng nhỏ, trả lời bằng bằng chứng; không cần đọc đoạn dài quá sức.",
        "My name is Lan. I am nine. My brother is seven. He likes cars. My sister is ten. She likes dolls. We are in the living room. I have a book and I like reading.",
        "Một người có nhiều đặc điểm; không ghép tuổi của người này với sở thích người kia.",
        "Tách ba người thành ba hàng.|Ghi tuổi và sở thích cho đúng hàng.|Kiểm tra toàn bộ điều kiện câu hỏi với câu trong đoạn.",
        """Lan bao nhiêu tuổi?|Nine|Seven|Ten|Lan nói I am nine.
Brother bao nhiêu tuổi?|Seven|Nine|Ten|My brother is seven.
Sister thích đồ chơi nào?|Dolls|Cars|Kites|She likes dolls nói về sister.
Brother thích đồ chơi nào?|Cars|Dolls|Balls|He likes cars nói về brother.
Các bạn đang ở đâu?|Living room|Bedroom|School|We are in the living room.
Lan thích làm gì?|Reading|Drawing|Swimming|Câu cuối nói I like reading.""",
        vip=True,
    ),
]
