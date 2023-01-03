import flet
from flet import (
    Page,
    TextField,
    FloatingActionButton,
    Column,
    Row,
    Text,
    IconButton,
    OutlinedButton,
    Tabs,
    Tab,
    UserControl,
    Checkbox,
    colors,
    icons,
)


class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, 
            label=self.task_name, 
            on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            icon_color = colors.YELLOW_900,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            icon_color = colors.RED,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )

        return Column(
            controls=[
                self.display_view, 
                self.edit_view
            ]
        )

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)


class TodoApplication(UserControl):
    def build(self):
        self.new_task = TextField(hint_text="List Your Works Here ...", expand=True)
        self.tasks = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="همه کارها"), Tab(text="انجام نشده ها"), Tab(text="تمام شده")],
        )

        self.items_left = Text("تمامی کارهایتان را انجام داده اید")

        return Column(
            width=600,
            controls=[
                Row(
                    [
                        Text(
                            value="Created By Ardavan", 
                            style="headlineMedium"
                        )
                    ], 
                    alignment="center"),
                
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(
                            icon=icons.ADD, 
                            on_click=self.add_clicked
                        ),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="پاکسازی کارهای انجام شده", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_status_change, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        
        for task in self.tasks.controls:
            task.visible = (
                status == "همه کارها"
                or (status == "انجام نشده ها" and not task.completed)
                or (status == "تمام شده" and task.completed)
            )
            
            if not task.completed:
                count += 1
                
        self.items_left.value = f"{count} Active Duty(s)"
        super().update()


def main(page: Page):
    page.title = "To-Do Application With Flet"
    page.horizontal_alignment = "center"
    
    page.window_width = 600
    page.window_height = 700
    page.window_resizable = False
    
    app = TodoApplication()

    page.add(app)


if __name__ == "__main__":
    flet.app(target=main)