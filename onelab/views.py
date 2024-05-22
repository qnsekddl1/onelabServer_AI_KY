from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

from file.models import File
from member.models import Member, MemberFile
from onelab.models import OneLab, OneLabFile, OneLabBannerFile
from onelabMember.models import OneLabMember
from university.models import University


class OnelabWriteView(View):
    def get(self, request):
        member = Member(**request.session['member'])
        university = University.objects.get(member=member)
        profile = MemberFile.objects.filter(member=member).first()

        context = {
            'member': member,
            'university': university,
            'profile': profile,
        }

        default_profile_url = 'https://static.wadiz.kr/assets/icon/profile-icon-1.png'

        if profile is None:
            profile = default_profile_url

        return render(request, "onelab/one-lab-write.html", context)

    @transaction.atomic
    def post(self, request):
        data = request.POST
        files = request.FILES.get('file-img')
        files_banner = request.FILES.get('file-banner')
        data = {
            "onelab_main_title": data['onelab-main-title'],
            "onelab_content": data['onelab-content'],
            "onelab_detail_content": data['onelab-detail-content'],
            "onelab_max_count": data['onelab-max-count'],
            "onelab_ask_email": data['onelab-ask-email'],
            "onelab_url": data['onelab-url'],
            "university": University.objects.get(member_id=request.session['member']['id'])
        }


        onelab = OneLab.objects.create(**data)

        if files is not None:
            file_instance = File.objects.create(file_size=files.size)
            OneLabFile.objects.create(onelab=onelab, file=file_instance, path=files)

        if files_banner is not None:
            file_instance = File.objects.create(file_size=files.size)
            OneLabBannerFile.objects.create(onelab=onelab, file=file_instance, path=files_banner)

        return redirect(onelab.get_absolute_url())

class OnelabDetailView(View):
    def get(self, request):
        onelab = OneLab.objects.get(id=request.GET.get('id'))
        onelab.updated_date = timezone.now()
        # members = list(onelab.onelabmember_set.all())
        members = OneLabMember.objects.filter(onelab=onelab)
        onelab_file = OneLabFile.objects.filter(onelab=onelab)
        onelab_banner_file = OneLabBannerFile.objects.filter(onelab=onelab)
        # print(members)

        # context = {
        #     'community': community,
        #     'community_file': CommunityFile.objects.filter(community=community),
        #     'profile': profile
        # }
        # 랩원
        return render(request, "onelab/one-lab-detail.html", {"onelab": onelab, "members": members, "onelab_file":onelab_file, "onelab_banner_file":onelab_banner_file})

    def post(self, request):
        data = request.POST
        member_id = request.session['member']['id']
        real_member = University.objects.get(member_id=member_id)
        onelab_id = int(data.get('onelab_id'))  # 문자열을 숫자로 변환
        print(onelab_id)

        datas = {
            'onelab_member_status': 1,
            'university_id': real_member.member_id,
            'onelab_id': onelab_id
        }
        if real_member.member_id == onelab_id:
            pass
        OneLabMember.objects.create(**datas)
        return redirect('onelab:list')

class OnelabListView(View):
    def get(self, request):
        onelabs = OneLab.enabled_objects.filter(onelab_post_status=True).order_by('-id')
        total_onelabs = onelabs.count()
        member_id = request.session['member']['id']

        for onelab in onelabs:
            onelab_member_count = OneLabMember.objects.filter(onelab_id=onelab.id, onelab_member_status=1).count()
            setattr(onelab, 'one_lab_member_count', onelab_member_count)

        context = {
            'member': request.session['member'],
            'onelab': onelabs,
            'total': total_onelabs,
        }

        return render(request, 'onelab/one-lab-list.html', context)

