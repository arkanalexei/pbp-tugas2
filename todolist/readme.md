## Link Heroku
https://tugas-2-pbp-arkan.herokuapp.com/todolist/

## Apa kegunaan {% csrf_token %} pada elemen <form>? Apa yang terjadi apabila tidak ada potongan kode tersebut pada elemen <form>?

CSRF atau Cross-Site Request Forgery token adalah merupakan sebuah cara agar sebuah aplikasi bisa menentukan apabila request HTTP tersebut merupakan benar dibuat oleh aplikasi tersebut. CSRF token sendiri adalah sebuah token dengan nilai random yang besar untuk menjamin keamanannya dan digunakan untuk mencegah penyerangan CSRF. Oleh karena itu, token tersebut harus unik untuk setiap user. Token tersebut dibuat unik untuk setiap session user dan disembunyikan parameter HTML untuk operasi-operasi server side yang kemudian dikirim ke browser klien. Sehingga ketika sebuah user melakukan sesuatu, aksi tersebut harus disertakan CSRF token sebagai alat verifikasi. Apabila CSRF token tidak dimasukkan, kita tidak tahu apabila request tersebut benar-benar dari user.
  
## Apakah kita dapat membuat elemen <form> secara manual (tanpa menggunakan generator seperti {{ form.as_table }})? Jelaskan secara gambaran besar bagaimana cara membuat <form> secara manual.
Ya, tentu saja bisa. Kenapa tidak memangnya? Saya buktikan bahwa kita bisa membuat form tanpa {{ form.as_table }} dengan kode html saya di app ini. Cara render form tersebut juga gampang. Pada salah satu fungsi views.py, saya menambahkan context dengan key 'form' dan value form dimana value form disini adalah UpdateForm(instance=queryset). Ini saya ambil contoh dari kode fungsi update_task(request, task_id) saya. Setelah dimasukkan di context, pada html anda (ini salah satu bagian kode update_task.html saya) anda referensikan variable form tersebut. Sehingga hasilnya kerender di html.
```html
<form method="POST" action="">{% csrf_token %}
		{{form}}
		<input class="btn btn-sm btn-success" type="submit" value="Update" name="Update">
	</form>
```
 
## Jelaskan proses alur data dari submisi yang dilakukan oleh pengguna melalui HTML form, penyimpanan data pada database, hingga munculnya data yang telah disimpan pada template HTML.
<ul>
    <li>Tampilkan form default yang user request. Apabila form ini baru, mungkin isi defaultnya kosong. Kalau tidak, mungkin sudah ada nilai lain.</li>
    <li>Mendapatkan data dari user melalui request submit</li>
    <li>Bersihkan dan validasi data tersebut</li>
    <li>Apabila ada data yang tidak valid, beri peringatan ke user mengenai data mana yang tidak valid dan prompt ulang</li>
    <li>Jika semua data valid, save data tersebut dan lakukan sesuai logic yang kita inginkan. Misal untuk form isi feedback, kirim isi feedback tersebut ke email kita. Kalau merupakan sebuah search, maka tampilkan hasil search. Atau dalam konteks tugas 3 ini maka buat task baru sesuai dengan input title dan description</li>
</ul>
Untuk penjelasan secara visual ada di bagan ini:<br>

![bagan](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms/form_handling_-_standard.png)
<br>
Sumber: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
### Membuat suatu aplikasi baru bernama todolist di proyek tugas Django yang sudah digunakan sebelumnya.
```
django-admin startapp todolist
```
### Menambahkan path todolist sehingga pengguna dapat mengakses http://localhost:8000/todolist.
urls.py di project_django, tambahkan
```py
path('todolist/', include('todolist.urls')),
```

### Membuat sebuah model Task yang memiliki atribut sesuai ketentuan soal
models.py di todolist
```py
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
```

### Mengimplementasikan form registrasi, login, dan logout agar pengguna dapat menggunakan todolist dengan baik.
Sama seperti pada lab 3. Pada views.py
```py
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form, 'user':request.user}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            response.set_cookie('username', username)
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return redirect('todolist:login')
```
Lalu pada urls.py
```py
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
```
Jangan lupa membuat login.html, register.html, dan update todolist.html biar bisa logout

### Membuat halaman utama todolist yang memuat username pengguna, tombol Tambah Task Baru, tombol logout, serta tabel berisi tanggal pembuatan task, judul task, dan deskripsi task.
```html
<!-- Membuat halaman utama todolist yang memuat username pengguna,
tombol Tambah Task Baru, tombol logout, serta tabel berisi tanggal pembuatan task, judul task,
dan deskripsi task. -->

{% extends 'base.html' %}

{% block content %}
<h3>Welcome back, {{username}}!</h3>

<h5>Sesi terakhir login: {{ last_login }}</h5>
<button><a href="{% url 'todolist:logout' %}">Logout</a></button>
<button><a href="{% url 'todolist:create-task' %}">Create Task</a></button>

<table>
    <tr>
      <th>Title</th>
      <th>Description</th>
      <th>Date</th>
      <th>User</th>
      <th>Status</th>
      <th>Toggle Status</th>
      <th>Delete Task</th>
    </tr>
    {% for task in tasks %}
        <tr>
            <th>{{task.title}}</th>
            <th>{{task.description}}</th>
            <th>{{task.date}}</th>
            <th>{{task.user}}</th>
            <th>{{task.is_finished}}</th>
            <th><a class="btn btn-sm btn-light" href="{% url 'todolist:update_task' task.id %}">Update</a></th>
            <th><a href="{% url 'todolist:delete_task' task.id %}">Delete</a>
        </tr>
    {% endfor %}
  </table>


{% endblock content %}
```

### Membuat halaman form untuk pembuatan task. Data yang perlu dimasukkan pengguna hanyalah judul task dan deskripsi task.
```html
{% extends 'base.html' %}

{% block content %}
<h3>Welcome back, {{user}}!</h3>


<form method="POST" action="">
    {% csrf_token %}
    <table>
        <tr>
            <td>Title: </td>
            <td><input type="text" name="title" placeholder="Nyuci baju" class="form-control"></td>
        </tr>
                
        <tr>
            <td>Description: </td>
            <td><input type="text" name="description" placeholder="Pakai deterjen biar bersih" class="form-control"></td>
        </tr>

        <tr>
            <td></td>
            <td><input class="btn login_btn" type="submit" value="Tambah Task Baru"></td>
        </tr>
    </table>
</form>


<button><a href="{% url 'todolist:logout' %}">Logout</a></button>
{% endblock content %}
```

### Membuat routing sehingga beberapa fungsi dapat diakses melalui URL sesuai ketentuan soal
urls.py
```py
urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create-task'),
    path('delete_task/<str:task_id>/', delete_task, name="delete_task"),
    path('update_task/<str:task_id>/', update_task, name="update_task"),

]
```

### Melakukan deployment ke Heroku terhadap aplikasi yang sudah kamu buat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
Proses ini sama persis seperti di tutorial. Pertama kita harus membuat app baru di Heroku. Lalu menambahkan secret yakni Heroku app name dan api key di secret repo kita. Lalu tinggal deploy deh!
### Membuat dua akun pengguna dan tiga dummy data menggunakan model Task pada akun masing-masing di situs web Heroku.
Register akun 1 --> login akun 1 --> Create 3 tasks --> logout <br>
Register akun 2 --> login akun 2 --> Create 3 tasks --> logout

# README Tugas 5

## Apa perbedaan dari Inline, Internal, dan External CSS? Apa saja kelebihan dan kekurangan dari masing-masing style?
Secara garis besar, ketiga hal ini adalah cara-cara berbeda dalam menerapkan CSS dalam HTML kita. Untuk inline, kita mendefinisikan styling CSS kita langsung di tag html tersebut. Contoh:<br>
```html
<h3 style="color:orange; font-style:italic; text-decoration: underline; ">Ada apa dengan Cicak (bin Kadal)?</h1>
```
Kelebihan Inline CSS:
<ol>
    <li>Quick and easy to apply</li>
    <li>Smaller HTTP request</li>
    <li>Bagus untuk menguji perubahan setiap element</li>
</ol>

Kekurangan Inline CSS:
<ol>
    <li>Tidak efisien karena hanya diterapkan ke satu elemen</li>
</ol>

<br>
Lalu internal CSS adalah dimana kita mendefinisikan styling CSS kita di tag html <style></style> didalam <head></head>. Sebagai contoh:<br>
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
        background-color: black;
        }
        h3 {
        color: blue;
        }
    </style>
</head>

<body>
    <!-- bla bla -->
</body>
</html>
```
Kelebihan Internal CSS:
<ol>
    <li>CSS diterapkan ke satu halaman</li>
    <li>Bisa menggunakan selector class dan id</li>
    <li>Tidak perlu menyediaka file css external</li>
</ol>

Kekurangan Internal CSS:
<ol>
    <li>Increase web access time</li>
    <li>CSS diterapkan ke satu halaman (ini kelebihan dan kekurangan karena tergantung situasi & kondisi)</li>
</ol>

<br>

Dan terakhir adalah external CSS dimana kita mendefinisikan styling CSS kita di file .css tersendiri sehingga kita harus "link" css ke html kita di <head></head>. Contoh:<br>

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">  
</head>
</html>
```
Sedangkan isi style.css adalah: <br>
```css
.card:hover {
    transform: scale(1.05);
    opacity: 0.9;
}
.card {
    margin-left: 20px;
    margin-right: 20px;
}

a {
    text-decoration: none;
    float: right;
    color: black;
  }
```
Kelebihan External CSS:
<ol>
    <li>Overall smaller HTML file dan struktur file lebih rapih</li>
    <li>Faster loading time</li>
    <li>Bisa reuse css yang sama di html lain</li>
</ol>

Kekurangan External CSS:
<ol>
    <li>Harus menunggu sampai file CSS selesai dipanggil agar kerender sempurna</li>
</ol>

## Jelaskan tag HTML5 yang kamu ketahui.
Ada banyak ya, mungkin saya coba list beberapa
<ol>
    <li>< h1 > ke < h6 > untuk heading 1 ke 6. Semakin besar angka, semakin kecil tulisannya</li>
    <li>< head > mendefisikan "kepala" html nya</li>
    <li>< body > mendefisikan "badan" html nya</li>
    <li>< nav > mendefisikan "navigasi" html nya, cenderung bentuk navbar</li>
    <li>< p > untuk paragraf </li>
    <li>< section > mendefinisikan section html</li>
    <li>< b > untuk bold</li>
    <li>< ol > definisikan ordered list</li>
    <li>< li > item dari list tersebut</li>
    <li>... Dan masih banyak lagi!</li>
</ol>

## Jelaskan tipe-tipe CSS selector yang kamu ketahui.
Beberapa yang saya ketahui:
<ol>
    <li>.class1 -> semua elemen dengan class=class1</li>
    <li>#id1 -> semua elemen dengan id=id1</li>
    <li>* -> semua elemen</li>
    <li>element (contoh p, h5, h2) -> semua elemen dengan tag html tersebut</li>
    <li>:hover -> ketika mouse hover diatas elemen tersebut</li>
    <li>.. Etc</li>
</ol>

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
### Kustomisasi templat untuk halaman login, register, dan create-task semenarik mungkin.
Untuk halaman login dan register saya mendapatkan inspirasi berat dari [codepen](https://codepen.io/ig_design/pen/KKVQpVP). Saya tinggal kustomisasi html serta css saya sehingga bisa terintegrasi dengan html orisinil saya yang disediakan oleh lab 4. Yang sedikit ribet itu di register.html karena form nya itu auto generated. Sehingga aku harus cari cara by opening inspect element di local, lalu baru copy input form nya. Untuk create task itu saya bikin secara sendiri. Tambahkan ini di create_task.html agar bisa pakai bootstrap dan external css
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
<link rel="stylesheet" href="{% static 'css/create_task.css' %}">
```
Setelah itu tinggal otak-atik css nya sampai saya puas dengan hasilnya. Done!

### Kustomisasi halaman utama todo list menggunakan cards. (Satu card mengandung satu task).
Tambahkan ini di todolist.html
```html
<div class="row row-cols-1 row-cols-md-4 g-4">
    {% for task in tasks %}
        <div class="col">
            <div class="card">
                {% if task.is_finished %}
                <div class="card-header text-bg-success text-center">Completed</div>
                {% else %}
                <div class="card-header text-bg-warning text-center">Not Yet Completed</div>
                {% endif %}

                <div class="card-body">
                    <h5 class="card-title">{{task.title}}</h5>
                    <p class="card-text">{{task.description}}</p>

                </div>
                <div class="card-footer">
                        <small class="text-muted text-center">Created {{task.date}} by {{task.user}}</small>
                        <a class="btn btn-sm btn-danger text-end" href="{% url 'todolist:delete_task' task.id %}">Delete</a>
                        <a class="btn btn-sm btn-primary text-end" href="{% url 'todolist:update_task' task.id %}">Update</a>
                        
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```
Basically bikin grid untuk letak card nya. Lalu untuk setiap task di tasks, bikin card dengan sedemikian rupa. Untuk bagian bonus tinggal tambahin selector :hover untuk card sebagai berikut (inside todolist.css)
```css
.card:hover {
    transform: scale(1.05);
    opacity: 0.9;
}
```

### Membuat keempat halaman yang dikustomisasi menjadi responsive.
By default menggunakan bootstrap sudah menjadi responsive. Jadi tidak perlu implement apa-apa lagi.