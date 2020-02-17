def parse_input(self):
    # 获取模版
    if self.input_content.strip() in ['模版', '模板']:
        self.output_content = template1
        return
    if self.input_content.strip() in ['模版2', '模板2']:
        self.output_content = template2
        return
    # 验证消息以+分割
    tmpt_1 = re.findall('\+', self.input_content)
    if len(tmpt_1) == 0:
        self.output_content = '连接符为+，请重新输。' + template1
        return
    # 验证消息数量必须要为8
    # 获取关键list -> content_list
    content_list = [x.strip() for x in self.input_content.split('+')]
    if len(content_list) != 8:
        self.output_content = '输入信息不完整，请重新输入。' + template1
    # 验证识别码
    if str(content_list[0]) != passwd:
        self.output_content = '识别码不正确，请重新录入。' + template1
        return
    # 验证车辆号
    tempt1 = content_list[1].split('-')[0].upper()
    tempt2 = content_list[1].split('-')[1].upper()
    print(tempt1)
    print(tempt2)
    try:
        self.project = Project.objects.get(project_name=tempt1)
    except (KeyError, Project.DoesNotExist):
        self.output_content = '项目号不存在，请重新录入或与工程师确认。' + template1
        self.project = None
        return
    try:
        self.vehicle = self.project.vehicle_set.get(vehicle_number=tempt2)
    except (KeyError, Vehicle.DoesNotExist):
        self.output_content = '车辆号不存在，请重新录入或与工程师确认。' + template1
        self.vehicle = None
        return
    # 验证时间格式
    for i in [3, 5]:
        tmpt = re.findall(':', content_list[i])
        if len(tmpt) != 1:
            self.output_content = '时间格式不正确，请重新录入。' + template1
            return
    self.output_content = '成功录入日报系统。'
    self.content = content_list
    self.uploading()