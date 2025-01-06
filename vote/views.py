from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import VoteData
from django.utils.timezone import now

def index(request):
    if request.method == "POST":
        # 获取访问者的 IP 地址
        visitor_ip = request.META.get('REMOTE_ADDR')

        # 获取该用户已经投的票数
        existing_votes = VoteData.objects.filter(visitor_ip=visitor_ip).count()

        # 如果用户已经投过 10 次票，则拒绝继续投票
        if existing_votes >= 20:
            messages.add_message(request, messages.ERROR, "Your device have reached the maximum number of votes. If you have any question, ask the staff. \n你的设备已经达到最大投票次数，如有任何问题欢迎联系工作人员。")
            return JsonResponse({})  # 重定向回原页面

        # 获取表单中的投票标志
        lflag = request.POST.get('lflag') == "true"
        pflag = request.POST.get('pflag') == "true"
        vflag = request.POST.get('vflag') == "true"
        
        # 验证表单数据的有效性
        if lflag or pflag or vflag:
            # 确保每个请求最多只能选择两票
            selected_votes = [flag for flag in [lflag, pflag, vflag] if flag]
            if len(selected_votes) != 2:
                messages.add_message(request, messages.ERROR,"You must vote for two houses.")
                return JsonResponse({})  # 重定向回原页面

            # 如果选择了Lyceum (lflag) 创建一条记录
            if lflag:
                VoteData.objects.create(house="l", visitor_ip=visitor_ip, creation_time=now())
            # 如果选择了Parnassus (pflag) 创建一条记录
            if pflag:
                VoteData.objects.create(house="p", visitor_ip=visitor_ip, creation_time=now())
            # 如果选择了Virtus (vflag) 创建一条记录
            if vflag:
                VoteData.objects.create(house="v", visitor_ip=visitor_ip, creation_time=now())
            
            messages.add_message(request, messages.SUCCESS,"Votes submitted successfully!\n您的投票已经成功提交，请不要重复提交，你可以将电子设备借给周围的人投票。但不要刷票，我们会实时检测并判无效票。")

            return JsonResponse({})  # 成功后重定向回原页面

        else:
            messages.add_message(request, messages.ERROR,"No valid votes selected.")

            return JsonResponse({})  # 重定向回原页面

    return render(request, "index2.html", locals())



def show(request):
    return render(request, "index.html", locals())

def get_data(request):
    # 获取每个学院的投票数量
    l = VoteData.objects.filter(house="l").count()
    p = VoteData.objects.filter(house="p").count()
    v = VoteData.objects.filter(house="v").count()

    # 构造投票数据和排名
    vote_data = [
        ("l", l),
        ("p", p),
        ("v", v)
    ]

    # 根据投票数排序（从高到低）
    sorted_votes = sorted(vote_data, key=lambda x: x[1], reverse=True)

    # 生成排名信息
    ranks = {}
    rank_mapping = {1: "1st", 2: "2nd", 3: "3rd"}

    # 为了处理相同票数的情况，记录排名
    current_rank = 1
    for i in range(len(sorted_votes)):
        if i > 0 and sorted_votes[i][1] == sorted_votes[i - 1][1]:
            # 如果当前票数和前一个相同，保持当前排名
            ranks[sorted_votes[i][0]] = ranks[sorted_votes[i - 1][0]]
        else:
            # 否则，更新为新的排名
            ranks[sorted_votes[i][0]] = rank_mapping[current_rank]
        current_rank += 1

    return JsonResponse({
        "count": l + p + v,      # 总票数
        "countl": l,             # Lyceum 的票数
        "countp": p,             # Parnassus 的票数
        "countv": v,             # Virtus 的票数
        "ppcountl": ranks["l"],  # Lyceum 的排名
        "ppcountp": ranks["p"],  # Parnassus 的排名
        "ppcountv": ranks["v"],  # Virtus 的排名
    })
