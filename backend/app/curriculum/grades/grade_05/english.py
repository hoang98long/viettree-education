"""Short original A1 reading contexts, guided language and speaking practice."""

from app.curriculum.grades.grade_05.builders import language_unit

ENGLISH = []


def add(topic, code, title, rule, text, rows, reflection=None):
    ENGLISH.append(
        language_unit(
            "ENGLISH",
            len(ENGLISH),
            topic,
            code,
            title,
            rule,
            text,
            "Đọc từ khóa và dấu hiệu thời gian. Dùng thông tin nhân vật giả định; luyện nói cùng người hướng dẫn, không cần kể dữ liệu riêng.",
            [
                "Tìm người, việc, nơi hoặc thời điểm được hỏi; gạch chân từ khóa trong đoạn.",
                rule,
                "Đọc lại cả câu chứa thông tin; kiểm tra yesterday, usually hoặc will trước khi chọn.",
            ],
            rows,
            reflection=reflection
            or [
                "Viết 30–40 từ theo mẫu bằng thông tin giả định, rồi nhờ người hướng dẫn giúp đọc lại."
            ],
        )
    )


add(
    "self",
    "profile-and-friends",
    "Introduce a friend: tên, tuổi và sở thích",
    "Dùng he/she và thông tin đã có để giới thiệu bạn. Where hỏi nơi, how old hỏi tuổi, what hỏi thông tin. Đọc toàn câu trước khi chọn, không đoán chỉ từ một từ quen.",
    "My name is Anna. I am ten years old. I live in Green Street with my parents and my brother. My friend Ben is in my class. He likes drawing animals, but I like reading stories. After school, we often go to the library together. On Fridays, we share a book with our friends. We keep the books clean and return them on time.",
    """
How old is Anna? | Ten | Twelve | Eight | Đoạn nêu I am ten years old.
Who is Ben? | Anna's classmate | Anna's brother | Anna's teacher | Ben is in Anna's class.
What does Ben like? | Drawing animals | Reading only maps | Cooking dinner | Đoạn nói He likes drawing animals.
Where do they often go after school? | The library | The airport | The hospital | Có câu we often go to the library together.
""",
)

add(
    "self",
    "where-you-live",
    "Where do you live? Đọc mô tả nơi ở",
    "Where do you live? hỏi nơi ở. Near, next to và opposite mô tả vị trí. Chỉ dùng dữ kiện giả định trong ngữ liệu, không cần nhập địa chỉ nhà thật.",
    "Tom lives in a small town near a river. His house is next to a bakery and opposite a park. Every morning, he walks to school with his sister. The school is not far from their home. At the weekend, Tom visits the park and reads under a big tree. He likes his town because it is quiet and people are friendly.",
    """
Where does Tom live? | In a small town | On a ship | In an airport | Đoạn mở đầu nêu a small town near a river.
What is next to his house? | A bakery | A hospital | A cinema | His house is next to a bakery.
How does Tom go to school? | On foot | By plane | By boat | Walks to school nghĩa là đi bộ.
Why does he like his town? | It is quiet and people are friendly | It is always very noisy | There are no trees | Câu cuối đưa lí do với because.
""",
)

add(
    "school",
    "daily-routine",
    "Daily routines: thời gian và hoạt động",
    "Hiện tại đơn mô tả hoạt động thường ngày. Với he/she, chú ý dạng động từ trong câu mẫu; at dùng với giờ. Tìm mốc thời gian để nối đúng người và việc.",
    "Mai gets up at six o'clock. She has breakfast with her family and goes to school at seven. Her first lesson starts at half past seven. At school, she enjoys English and music. In the afternoon, she does her homework and helps her brother read. She usually goes to bed at nine. Mai likes this routine because she has time to learn and rest.",
    """
When does Mai get up? | At six o'clock | At nine o'clock | At half past seven | Câu đầu nêu giờ thức dậy.
What starts at half past seven? | Her first lesson | Her dinner | Her bedtime | Câu thứ ba nói first lesson starts.
Who does she help read? | Her brother | Her driver | Her doctor | Ngữ liệu nói helps her brother read.
Why does she like her routine? | She has time to learn and rest | She never rests | She misses every lesson | Câu cuối nêu lí do cụ thể.
""",
)

add(
    "school",
    "frequency",
    "Usually, often, never: thói quen",
    "Always, usually, often, sometimes, never cho biết tần suất. Không hiểu never như sometimes. Tìm hoạt động đi với trạng từ; số lần trong lịch giúp hiểu how often.",
    "Our class has a reading club on Tuesdays and Thursdays. Ben usually brings a storybook. Anna sometimes brings a book about animals. We always put the books back after reading. We never write on library books. On other days, we can read at home. Our teacher often asks us to share one interesting detail. The club helps us enjoy reading and care for books.",
    """
How often is the club? | Twice a week | Every morning | Once a month | Tuesdays and Thursdays là hai ngày mỗi tuần.
What does Ben usually bring? | A storybook | A football | A cooking pot | Câu nêu Ben usually brings a storybook.
What do they never do? | Write on library books | Put books back | Read at home | Never write on library books là việc không làm.
What does the teacher often ask? | Share an interesting detail | Throw books away | Skip all reading | Câu gần cuối nói share one interesting detail.
""",
)

add(
    "health",
    "feelings-health",
    "Health words: đọc và nói khi cần giúp",
    "I have a headache/sore throat diễn đạt điều khó chịu trong câu mẫu. Hỏi What's the matter? để biết bạn cần giúp. Nội dung luyện từ vựng, không tự chẩn đoán; khi không khỏe hãy báo người lớn.",
    "Ben does not feel well today. He has a headache and tells his teacher. The teacher asks him to sit in a quiet place while she calls his father. Anna brings Ben his schoolbag. Ben will go home with his father and rest. He thanks Anna and the teacher. The class knows that telling an adult is important when someone does not feel well.",
    """
What's the matter with Ben? | He has a headache | He lost a bike | He is hungry at a picnic | Đoạn nói he has a headache.
Who does Ben tell first in the text? | His teacher | A pilot | A shopkeeper | Câu đầu nêu tells his teacher.
Who will take him home? | His father | Anna alone | A stranger | Câu Ben will go home with his father.
What is the class reminded to do when unwell? | Tell an adult | Hide the problem | Diagnose themselves from a story | Câu cuối nêu telling an adult is important.
""",
)

add(
    "health",
    "should-advice",
    "Should và lời đề nghị đơn giản",
    "Should + động từ nguyên mẫu đưa lời khuyên đơn giản; Could you...? là lời đề nghị lịch sự. Dựa vào tình huống để chọn, không thêm tên thuốc hoặc cách điều trị.",
    "The class is preparing for a hot afternoon outside. The teacher says, 'You should bring water and a hat. You should stay with your group.' Anna asks, 'Could you help me carry this bag, please?' Ben says yes. If a child feels unwell, the group will tell the teacher. They will stop and ask an adult for help rather than trying to solve a health problem alone.",
    """
What should children bring? | Water and a hat | A heavy television | Medicine for everyone | Câu mẫu đưa water and a hat cho buổi ngoài trời.
Could you help me...? is what kind of sentence? | A polite request | An insult | A statement about yesterday | Could you cùng please tạo lời đề nghị lịch sự.
Who should the group stay with? | Their group and teacher | Any stranger | No one | Hướng dẫn stay with your group.
What will they do if someone feels unwell? | Tell the teacher and ask an adult | Guess a treatment alone | Leave the child behind | Đoạn kết nêu việc báo người lớn.
""",
)

add(
    "travel",
    "transport",
    "By bus, by bike, on foot",
    "By + phương tiện diễn đạt cách đi; on foot là đi bộ. How hỏi cách thức, when hỏi lúc nào, where hỏi nơi. Chú ý người và phương tiện trong cùng câu.",
    "On Saturday, Anna and her family will visit a museum. They will go by bus because the museum is far from their home. Ben lives near the museum, so he will walk there with his mother. The families will meet at the entrance at nine o'clock. They will look at old objects and read the signs. After the visit, they will have lunch together.",
    """
Where will the families visit? | A museum | An airport | A farm | Câu đầu nói visit a museum.
How will Anna's family go? | By bus | By plane | On foot | Đoạn nêu they will go by bus.
Why will Ben walk? | He lives near the museum | He has no mother | The museum is in another country | Dữ kiện Ben lives near the museum giải thích cách đi.
When will they meet? | At nine o'clock | At midnight | At three o'clock | Câu nói meet at the entrance at nine o'clock.
""",
)

add(
    "travel",
    "directions",
    "Chỉ đường theo lời hướng dẫn",
    "Go straight, turn left/right là chỉ dẫn đơn giản. Next to, opposite giúp xác định vị trí. Đọc theo thứ tự; không đổi trái/phải theo điều mình đoán.",
    "Tom asks how to get to the library. A teacher says, 'Go straight from the school gate. Turn left at the bakery. The library is next to the park, opposite a small shop.' Tom repeats the directions to check them. He will go with his father after school. They will use the crossing and wait for the green light before crossing the road.",
    """
Where does Tom want to go? | The library | The airport | The beach | Câu đầu hỏi how to get to the library.
Where should he turn left? | At the bakery | At the school desk | At the river | Hướng dẫn nêu turn left at the bakery.
What is opposite the library? | A small shop | A mountain | A bus driver | Ngữ liệu nói opposite a small shop.
Why does Tom repeat the directions? | To check he understood | To change the road | To avoid going with his father | Đoạn nêu repeats the directions to check them.
""",
)

add(
    "nature",
    "seasons-weather",
    "Seasons and weather: chọn việc phù hợp",
    "Từ mùa và thời tiết giúp hiểu hoạt động. Because nêu lí do; will + động từ nói dự định sắp tới. Câu nói về vùng trong ngữ liệu, không khẳng định mọi nơi có thời tiết giống nhau.",
    "In Anna's town, summer is often hot and winter is cold. She likes spring because flowers grow in the park. This weekend, the weather report says it will rain. Anna will read at home instead of playing outside. Her brother will draw a picture of the rainy garden. If they need to go out, their parents will help them prepare for the weather.",
    """
Why does Anna like spring? | Flowers grow in the park | It is always snowy | The park has no plants | Có câu she likes spring because flowers grow.
What is summer like in the text? | Often hot | Always icy | Always dark | Câu đầu mô tả summer is often hot.
What will the weather be this weekend? | Rainy | Definitely snowy | Very dry according to the report | Bản tin trong ngữ liệu says it will rain.
What will Anna do? | Read at home | Fly alone to another town | Play outside in the rain | Đoạn nêu she will read at home.
What will her brother draw? | A rainy garden | A desert with no water | A school bus | Dữ kiện draw a picture of the rainy garden.
Does the paragraph describe every town? | No, it describes Anna's town | Yes, all places are the same | Yes, every season everywhere is identical | Câu đầu giới hạn In Anna's town.
""",
)

add(
    "stories",
    "past-weekend",
    "Yesterday: kể hoạt động đã diễn ra",
    "Yesterday, last Sunday báo việc đã xảy ra. Các dạng went, visited, played là quá khứ trong câu mẫu. Câu hỏi Did... dùng động từ nguyên mẫu; đọc dữ kiện trước khi trả lời.",
    "Last Sunday, Ben visited his grandparents. He went there by bus with his parents. In the morning, he helped his grandfather water the flowers. After lunch, he played chess with his grandmother. Ben did not watch television because he wanted to spend time with his family. Before leaving, he thanked his grandparents and promised to visit again. He felt happy on the way home.",
    """
Who did Ben visit? | His grandparents | A new teacher | A bus company | Câu đầu nêu visited his grandparents.
How did he go there? | By bus with his parents | Alone by plane | By boat with strangers | Câu thứ hai đưa cách đi và người đi cùng.
What did he do in the morning? | Watered flowers with his grandfather | Watched television all morning | Played football at school | Ngữ liệu nêu helped his grandfather water the flowers.
Who played chess with him? | His grandmother | His driver | Anna | After lunch, he played chess with his grandmother.
Why did he not watch television? | He wanted time with family | The television was stolen | He was at school | Lí do có sau because, không thêm chuyện ngoài bài.
How did he feel on the way home? | Happy | Angry | Lost | Câu cuối nêu felt happy.
""",
)

add(
    "stories",
    "future-holiday",
    "Will: kế hoạch cho kì nghỉ",
    "Will + động từ nguyên mẫu diễn đạt điều sẽ làm. Won't là will not. Một kế hoạch trong ngữ liệu là dự định, không phải việc đã xảy ra; hỏi when/what/where để lấy thông tin.",
    "Next month, Mai will visit the seaside with her family. They will stay for two days. Mai will take a book and draw pictures of the boats. Her brother will build a small sandcastle with their parents nearby. They won't leave rubbish on the beach. Before the trip, the family will check the weather and prepare their bags. Mai is excited about the holiday.",
    """
When will Mai visit the seaside? | Next month | Last Sunday | Yesterday | Next month là mốc thời gian tương lai.
How long will they stay? | Two days | Two years | One hour | Đoạn nêu stay for two days.
What will Mai take? | A book | A television | A pet elephant | Có câu Mai will take a book.
What will her brother build? | A small sandcastle | A large airport | A bus station | Ngữ liệu nêu build a small sandcastle.
What won't they do? | Leave rubbish on the beach | Check the weather | Prepare their bags | Won't leave rubbish là việc họ không làm.
Which form correctly follows will? | Visit | Visited | Visits | Will đi với động từ nguyên mẫu.
""",
)

add(
    "food",
    "food-and-quantity",
    "Food and drinks: đọc số lượng",
    "How many dùng với vật đếm được; how much với lượng như water. Đọc tên món và số lượng trong danh sách. Đây là luyện ngôn ngữ và phép đọc số, không cần mua đồ thật.",
    "For the class picnic, Anna prepares a list. The group needs six sandwiches, four apples and two bottles of water. Ben will bring cups, and Mai will bring a small bag for rubbish. The teacher will check the list before they leave. No one will take food that a family has said they cannot eat. The group will share politely and keep the picnic place clean.",
    """
How many sandwiches does the group need? | Six | Four | Two | Danh sách ghi six sandwiches.
How many apples are on the list? | Four | Six | Ten | Danh sách ghi four apples.
Who will bring cups? | Ben | Anna's driver | A shopkeeper | Có câu Ben will bring cups.
What will Mai bring? | A small bag for rubbish | Six bicycles | A television | Mai will bring a small bag for rubbish.
Why does the teacher check the list? | To prepare before leaving | To change the day to yesterday | To stop all sharing | Việc kiểm tra danh sách hỗ trợ chuẩn bị đúng đồ trước chuyến đi.
Which question fits apples? | How many apples? | How much apples? | Where much apples? | Apples là danh từ đếm được nên dùng how many.
""",
)

add(
    "self",
    "dream-job",
    "Dream jobs: nghề nghiệp và lí do",
    "What would you like to be? hỏi nghề muốn làm; I'd like to be... diễn đạt ước mơ. Because đưa lí do. Ước mơ có thể thay đổi và không dùng để xếp hạng bạn nào tốt hơn.",
    "Ben would like to be an artist because he enjoys drawing. Anna would like to be a teacher because she likes helping younger children learn. Mai is interested in being a farmer and growing vegetables. The friends talk about their dreams, but they know they can learn about many different jobs. Their teacher says that every useful job needs care, practice and responsibility.",
    """
What would Ben like to be? | An artist | A pilot | A driver | Câu đầu nói would like to be an artist.
Why would Anna like to teach? | She likes helping children learn | She dislikes all books | She only wants to fly | Lí do theo because là giúp trẻ học.
Which job interests Mai? | Farmer | Artist | Teacher | Câu nêu being a farmer and growing vegetables.
What can the friends learn about? | Many different jobs | Only one job forever | No jobs | Đoạn nói they can learn about many different jobs.
What does every useful job need in the text? | Care, practice and responsibility | Only expensive clothes | No learning | Câu cuối đưa ba điều cần thiết.
Which phrase politely expresses a dream? | I'd like to be a teacher | I teacher yesterday | I will teachered | I'd like to be đi với tên nghề phù hợp.
""",
)

add(
    "stories",
    "postcard-evidence",
    "VIP reading: a postcard with clues",
    "Đọc bưu thiếp để biết người viết đang kể việc đã làm hay dự định. Một suy luận cần có từ khóa hoặc câu làm bằng chứng; không thêm nơi hoặc việc chưa được nêu.",
    "Dear Ben, Yesterday our family visited a small museum near the sea. I saw old fishing boats and took notes about them. Today it is rainy, so we will read at the hotel. Tomorrow we will visit the market if our parents decide the weather is good. I bought a postcard for you yesterday. It is on my table. See you soon, Anna.",
    """
What did Anna visit yesterday? | A small museum | A new airport | Ben's classroom | Bưu thiếp mở bằng Yesterday... visited a small museum.
What did she take notes about? | Old fishing boats | School uniforms | A train timetable | Saw old fishing boats and took notes about them.
Why will they read at the hotel today? | It is rainy | They lost all books | The museum is inside the hotel | Because rainy được nêu với so we will read.
What is planned for tomorrow? | A market visit if weather is suitable | A definite flight alone | A school examination | Kế hoạch phụ thuộc quyết định của cha mẹ về thời tiết.
Is tomorrow's market visit certain from the text? | No, it depends on the parents' decision | Yes, no condition is given | Yes, because yesterday was sunny | Câu có if và điều kiện, không khẳng định đã chắc diễn ra.
Who is the postcard written to? | Ben | Mai | A doctor | Dòng Dear Ben cho biết người nhận.
Which word signals a completed past event? | Yesterday | Tomorrow | Will | Yesterday đi với việc đã diễn ra.
Which detail cannot be concluded? | The exact price of the postcard | Anna saw fishing boats | Today is rainy | Ngữ liệu không nói giá bưu thiếp.
""",
)

add(
    "food",
    "shopping-dialogue",
    "VIP dialogue: choose items from a list",
    "Đọc hội thoại theo người nói và yêu cầu. How many hỏi số vật; would like diễn đạt mong muốn lịch sự. Chọn theo danh sách, không theo món em thích ngoài bài.",
    "Anna: We'd like four apples and two bottles of water, please. Seller: Would you like oranges too? Anna: No, thank you. We have oranges at home. Ben: Could we have one small bag for the apples? Seller: Yes. Please check your list. Ben: There are three things on our list: apples, water and a bag. Anna: Thank you. We will carry everything carefully and take the bag home.",
    """
How many apples do they want? | Four | Two | One | Anna yêu cầu four apples.
How many bottles of water? | Two | Four | Three | Anna yêu cầu two bottles of water.
Why do they not buy oranges? | They have oranges at home | Oranges are not fruit | The seller has no apples | Anna đưa lí do có oranges at home.
What does Ben politely ask for? | One small bag | A large television | Four buses | Could we have one small bag... là lời đề nghị.
How many types of things are on the list? | Three | Seven | Two | Ben liệt kê apples, water and a bag, ba loại.
Which phrase is a polite refusal? | No, thank you | Give it now | You are wrong | No, thank you từ chối lịch sự trong hội thoại.
Will they leave the bag behind? | No, they will take it home | Yes, the text says so | Yes, because it is small | Câu cuối nêu take the bag home.
What should they check before leaving the shop? | The list and the items | Someone else's private address | The weather last year | Seller nhắc check your list, hợp với việc mua đúng đồ.
""",
)

add(
    "travel",
    "trip-plan",
    "VIP planning: time, place and transport",
    "Ghi giờ và hoạt động thành bảng nhỏ để so sánh. At đi với giờ, by với phương tiện. Lịch trong bài đã có dữ kiện; không cần tự đoán thời gian di chuyển chưa nêu.",
    "The class will leave school by bus at eight o'clock. They will reach the museum at nine and stay until eleven. Lunch will be at a park next to the museum. At twelve, the class will start the journey back and reach school at one. The teacher asks everyone to bring a notebook and stay with the group. Ben checks that he has his notebook before leaving home.",
    """
When will the class leave school? | At eight | At nine | At twelve | Câu đầu nêu leave school at eight.
How will they travel? | By bus | By plane | By boat | Câu đầu có by bus.
How long is the museum visit? | Two hours | Four hours | Thirty minutes | Từ nine đến eleven là hai giờ.
Where will lunch be? | At a nearby park | Back at school | In an airport | Đoạn nêu park next to the museum.
When will they start returning? | At twelve | At eight | At eleven exactly | Câu At twelve... start the journey back.
When will they reach school? | At one | At twelve | At nine | Lịch ghi reach school at one.
What should each child bring? | A notebook | A bicycle | A cooking pot | Teacher asks bring a notebook.
What must Ben check before leaving? | His notebook | The price of a bus | A weather report not mentioned | Câu cuối nêu Ben kiểm tra đã có notebook.
""",
)

add(
    "school",
    "club-schedule",
    "VIP inference: read a club timetable",
    "Đọc lịch theo từng ngày và điều kiện tham gia. Từ only giới hạn; từ before/after giúp thứ tự. Không suy ra hai hoạt động cùng giờ chỉ vì chúng gần nhau trong đoạn.",
    "Our clubs meet after school. The reading club is on Monday from three to four. The art club is on Wednesday at the same time. The music club meets only on Friday, from half past three to four. Anna wants to join reading and art. Ben wants music, but he will check with his parents first. All children must return shared materials before they leave the room.",
    """
When is the reading club? | Monday, three to four | Wednesday, three to four | Friday, three to four | Đoạn đưa ngày và giờ của reading club.
When is the art club? | Wednesday | Monday | Every day | Art club is on Wednesday.
How long is the music club? | Thirty minutes | One hour | Two hours | Từ half past three đến four là 30 phút.
Which clubs does Anna want? | Reading and art | Music only | All three | Đoạn nêu wants to join reading and art.
What will Ben do first? | Check with his parents | Leave without telling anyone | Join a club not mentioned | Ben will check with his parents first.
What does only on Friday tell us? | Music is not listed for other days | All clubs meet on Friday | Music meets every day | Only giới hạn ngày của music club trong lịch.
Can Anna attend reading and art according to the listed days? | Yes, they are on different days | No, both are Monday | No, both are Friday | Hai ngày Monday và Wednesday khác nhau.
What must children do before leaving? | Return shared materials | Keep every shared item | Change the timetable alone | Câu cuối nêu return shared materials.
""",
)

add(
    "nature",
    "environment-plan",
    "VIP reasoning: advice and a green plan",
    "Should nêu lời khuyên, will nêu việc dự định thực hiện. Dùng because để giải thích lí do bằng dữ kiện trong bài. Phân biệt một đề nghị với việc đã làm xong.",
    "The class will clean the small garden on Saturday. They should wear hats and bring water. Anna will collect paper, and Ben will water the plants with a teacher. Mai says they should use only the water the plants need because wasting water is not helpful. The group will put rubbish in the right bins. They will write a short report after the work and share it on Monday.",
    """
When will the work happen? | Saturday | Monday last week | Yesterday | Câu đầu nói on Saturday.
What will Anna do? | Collect paper | Water plants alone | Drive a bus | Đoạn phân công Anna collect paper.
Who will water plants with a teacher? | Ben | Anna | A stranger | Ben will water the plants with a teacher.
Why use only needed water? | To avoid wasting water | To make all plants dry | To fill every bin with water | Lí do theo because là wasting water is not helpful.
Which sentence expresses advice? | They should wear hats | Anna collected paper yesterday | The report was lost | Should wear hats là lời khuyên.
Which sentence describes a future plan? | They will write a report | They wrote it last month | They never write | Will write chỉ việc dự định sắp làm.
""",
)

add(
    "self",
    "polite-interview",
    "VIP speaking: interview a friend politely",
    "Could you...?, would you like...? giúp mở lời lịch sự. Câu trả lời cần đúng điều được hỏi. Luyện đóng vai với thông tin giả định, người hướng dẫn đọc chậm; bài chọn đáp án này chưa chấm phát âm.",
    "Anna: Could you tell me about your favourite school activity? Ben: I like the art club because I can draw with friends. Anna: How often do you go? Ben: Once a week, on Wednesdays. Anna: What would you like to try next term? Ben: I'd like to learn music. Anna: Thank you for sharing. Ben: You're welcome. They speak slowly and listen to each other without interrupting.",
    """
What is Ben's favourite activity? | The art club | The music club already | The bus trip | Ben nói I like the art club.
Why does he like it? | He can draw with friends | He never meets friends | He can skip school | Câu because I can draw with friends nêu lí do.
How often does he go? | Once a week | Every day | Twice a day | Ben nói once a week, on Wednesdays.
What would he like to try next term? | Music | Cooking at a shop | Driving | Ben says I'd like to learn music.
What makes the opening polite? | Could you tell me...? | Tell me now! | You must answer everything! | Could you là cách đề nghị lịch sự trong hội thoại.
How do they listen? | Without interrupting | By cutting every sentence | By walking away | Câu cuối mô tả cách nghe theo lượt.
""",
    ["Đóng vai hội thoại với người hướng dẫn bằng thông tin giả định; nói chậm và nghe hết lượt."],
)

add(
    "stories",
    "small-kindness",
    "VIP story: actions, reasons and ending",
    "Theo dõi who, what và why trong truyện ngắn. Một kết luận về nhân vật cần hành động làm bằng chứng. Có thể kể lại vài câu ở quá khứ, tránh thêm việc không xuất hiện.",
    "Yesterday, Tom found a small book near the school gate. He opened the first page and saw Anna's name. Tom did not keep the book. He took it to the teacher because he wanted to return it safely. After class, Anna came to collect it and thanked him. Tom felt happy that the book was back with its owner. The teacher asked the class to label their books clearly.",
    """
Where did Tom find the book? | Near the school gate | At an airport | In his kitchen | Câu đầu nêu near the school gate.
How did he know whose book it was? | He saw Anna's name | He guessed from the price | A stranger sold it | Câu thứ hai nêu saw Anna's name.
Why did he take it to the teacher? | To return it safely | To hide it from Anna | To sell it | Vì he wanted to return it safely.
When did Anna collect the book? | After class | Before it was found | Next year | After class, Anna came to collect it.
What can we infer about Tom from his action? | He tried to help return the book | He wanted to keep every book | He disliked all classmates | Không giữ lại, đưa cho teacher là bằng chứng giúp người.
What did the teacher ask the class to do? | Label books clearly | Remove all names | Leave books at the gate | Câu cuối nêu label their books clearly.
""",
)
