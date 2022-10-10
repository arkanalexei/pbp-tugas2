## Asynchronous programming vs Synchronous programming
Secara garis besar, pemrograman asinkronus itu memungkinkan untuk beberapa proses berjalan sekaligus. Dimana sinkronus program tersebut untuk menyelesaikan sebuah satu task terdahulu lalu baru lanjut ke task berikutnya. Misal ada 2 thread (A dan B) dalam sebuah prgoram. Dalam asinkronus, thread A dan B bisa berjalan dan selesai kapan saja tanpa menunggu thread satunya selesai eksekusi. Sedangkan pada sinkronus apabila thread A sedang berjalan, maka thread B harus menunggu hingga selesai baru bisa berjalan dan begitupula sebaliknya.

Asinkronus bisa meningkatkan throughput karena tidak harus menunggu. Namun sinkronus lebih metodikal dan presisi. Contoh nyata dari asinkronus adalah user interface yang responsive. Atau misalnya ketika user klik sebuah tombol untuk generate gambar random. Sembari menunggu gambar tersebut diambil, tempat gambar tersebut akan ditampilkan bisa dipersiapkan dahulu. Jadi dua proses yakni mengambil gambar dan menampilkan tempat berjalan bersamaan. Contoh sinkronus adalah ketika kita mengembangkan app untuk bermain catur. Karena pada dasarnya catur itu turn-based game, kita terpaksa untuk menunggu hingga lawan kita selesai bergerak agar kita bisa bergerak. Coba bayangkan apabila catur dimainkan secara asinkronus? 🤠

## Jelaskan maksud dari paradigma Event-Driven Programming dan contohnya di tugas ini
Paradigma event-driven programming menyatakan bahwa flow atau alur dari sebuah program itu bergantung pada event yang diperoleh dari action oleh user. Contoh-contoh action ini adalah mouse click atau hover, click enter, dan lain-lain yang bisa menjadi input. Paradigma ini prevalen pada aplikasi-aplikasi GUI. Hal ini karena pada umumnya GUI membutuhkan input dari user agar bisa berjalan. Contohnya aplikasi kalkulator. Tanpa input dari user maka yang muncul hanya kotak dengan berbagai angka serta simbol. Namun ditambah dengan fungsionalitas onclick, kalkulatornya bisa dipakai. Beberapa tipe mouse event yang ada di JavaScript adalah onclick, oncontextmenu, ondblclick, onmousedown, onmouseup, onmouseover, dan lain-lain. Dan itu baru dari mouse saja! Kita belum melihat keyboard event, animation event, progress event, dan lain-lain.

## Jelaskan penerapan asynchronous programming pada AJAX
Dengan AJAX, kita bisa mengambil data dari backend tanpa reloading atau mengirim dan menerima data dari server secara asinkronus. Penerapan nya secara nyata juga sebenarnya tidak terlalu sulit (namun syntaxnya saja perlu waktu untuk menyesuaikan).
```javascript
// AJAX GET
function getExample() {
            $.get("{% url 'todolist:show_json' %}", function (data) {
                $.each(data, function (i, value) {
                    // do something for each data
            })
        }

// AJAX DELETE (But using AJAX POST)
function deleteTask(pk) {
            var url = `/todolist/delete/${pk}/`;
            $.ajax({
                url: `/todolist/delete/${pk}/`,
                type: "POST",
                data: {},
                success: function (result) {
                    // do something when succeed
                },

                error: function (xhr, resp, text) {
                    // do something when error
                }
            });
        }

```
Sedangkan pada views.py nya
```python
@login_required(login_url='/todolist/login/')
def show_json(request):
    tasks = Task.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")

@login_required(login_url='/wishlist/login/')
@csrf_exempt
def todolist_delete(request, task_id):
    if request.method == "POST":
        data = get_object_or_404(Task, pk=task_id, user=request.user)
        data.delete()
        
    return HttpResponse()
```
Dengan ini, kita bisa mengupdate data dalam website tanpa reload.

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
### AJAX GET
#### Buatlah view baru yang mengembalikan seluruh data task dalam bentuk JSON.
Dalam views.py
```python
@login_required(login_url='/todolist/login/')
def show_json(request):
    tasks = Task.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", tasks), content_type="application/json")
```
#### Buatlah path /todolist/json yang mengarah ke view yang baru kamu buat.
Tambahkan pada urlpatterns di urls.py
```python
path('json/', show_json, name='show_json'),
```
#### Lakukan pengambilan task menggunakan AJAX GET.
Dalam todolist.html. Basically get data dari json tadi lalu build the cards.
```javascript
var container = document.createElement("div");
        container.classList.add("row", "row-cols-1", "row-cols-md-4", "g-4");

        function getTask() {
            container.innerHTML = "";
            $.get("{% url 'todolist:show_json' %}", function (data) {
                
                $.each(data, function (i, value) {
                    // iterate per task

                    var field = value.fields;
                    console.log("yez",value);

                    var col = document.createElement("div");
                    col.classList.add("col");

                    var card = document.createElement("div");
                    card.classList.add("card");
                    col.appendChild(card);

                    var header = document.createElement("div");
                    if (field.is_finished == true) {
                        header.classList.add("card-header", "text-bg-success", "text-center");
                        header.innerHTML = "Completed";
                    } else {
                        header.classList.add("card-header", "text-bg-warning", "text-center")
                        header.innerHTML = "Not Yet Completed";
                    }

                    var body = document.createElement("div");
                    body.classList.add("card-body");
                    var title = document.createElement("h5");
                    title.classList.add("card-title");
                    title.innerHTML = field.title;
                    var desc = document.createElement("p");
                    desc.classList.add("card-text");
                    desc.innerHTML = field.description;

                    body.appendChild(title);
                    body.appendChild(desc);

                    var footer = document.createElement("div");
                    footer.classList.add("card-footer");

                    card.appendChild(header);
                    card.appendChild(body);
                    card.appendChild(footer);

                    var date = document.createElement("small");
                    date.classList.add("text-muted", "text-center");
                    date.innerHTML = `Created ${field.date}`;

                    var updateBtn = document.createElement("a");
                    updateBtn.classList.add("btn", "btn-primary", "btn-sm", "text-end");
                    updateBtn.innerHTML = "Update";
                    updateBtn.href = "/todolist/update_task/" + value.pk + "/";

                    var deleteBtn = document.createElement("a");
                    deleteBtn.classList.add("btn", "btn-danger", "btn-sm", "text-end");
                    deleteBtn.innerHTML = "Delete";
                    deleteBtn.setAttribute('onclick', `deleteTask(${value.pk})`);

                    footer.appendChild(date);
                    footer.appendChild(deleteBtn);
                    footer.appendChild(updateBtn);

                    container.appendChild(col);
                })

                document.body.appendChild(container)

            })
        }
```
### AJAX POST
#### Buatlah sebuah tombol Add Task yang membuka sebuah modal dengan form untuk menambahkan task.
```html
<!-- Button -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
    Create Task
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Create Task</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form method="POST" action="" id="createTask">
                    {% csrf_token %}
                    <div class="mb-3">
                        <input type="text" name="title" placeholder="Task Title" class="form-control">
                    </div>
                    <div class="mb-3">
                        <input type="text" name="description" placeholder="Task Description" class="form-control">
                    </div>
                    <div class="mb-3">
                        <input class="btn login_btn btn-xl btn-primary" type="submit" value="Create Task">
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
```
#### Buatlah view baru untuk menambahkan task baru ke dalam database.
Dalam views.py
```python
@login_required(login_url='/wishlist/login/')
def todolist_add(request):
    if request.method == "POST":
        data = json.loads(request.POST['data'])

        new_task = Task(title=data["title"], description=data["description"], user=request.user)
        new_task.save()

        return HttpResponse(serializers.serialize("json", [new_task]), content_type="application/json")

    return HttpResponse()
```
#### Buatlah path /todolist/add yang mengarah ke view yang baru kamu buat.
Tambahkan pada urlpatterns di urls.py
```python
path('add/', todolist_add, name='todolist_add'),
```
#### Hubungkan form yang telah kamu buat di dalam modal kamu ke path /todolist/add
Inside todolist.html saya define document on ready sebagai berikut. Menghubungkan form di modal dengan /todolist/add melalui id dari formnya yakni createTask
```javascript
$(document).ready(function () {

            // GET
            getTask()

            // POST
            $("#createTask").submit(function (e) {
                e.preventDefault();
                console.log("oi oi oi")
                var actionurl = e.currentTarget;
                var formJSON = JSON.stringify($("#createTask").serializeJSON());
                console.log("e", e)
                console.log("json", formJSON)
                console.log("actionurl", actionurl)

                $.ajax({
                    type: "POST",
                    url: "{% url 'todolist:todolist_add' %}",
                    data: {
                        data: formJSON,
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                    },

                    success: function (response) {
                        $(response).each(function (i, value) {
                            
                        });
                        $('#createTask').each(function () {
                            this.reset();
                        });
                        console.log("mantap sukses");
                        getTask();

                        $('#exampleModal').modal('toggle');
                    },

                    error: function (xhr, resp, text) {
                        console.log("ada error")
                        console.log("xhr", xhr)
                        console.log("resp", resp)
                        console.log("text", text)
                    }
                });

            });

        });
```
#### Tutup modal setelah penambahan task telah berhasil dilakukan.
Ketika success, tambahkan kode ini. Jadi dari yang terbuka kita toggle supaya tutup kembali. exampleModal itu id dari modal nya.
```javascript
$('#exampleModal').modal('toggle');
```
#### Lakukan refresh pada halaman utama secara asinkronus untuk menampilkan list terbaru tanpa reload seluruh page.
Menggunakan fungsi getTask() yang sudah didefinisikan diatas.