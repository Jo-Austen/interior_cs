<script setup lang="ts">
import { reactive, computed, ref } from 'vue'
import { useApi } from '../../composables/useApi'
import {
    UFormField, USelect, UInput, UTextarea, UCheckbox,
    UCard, UBadge, UAlert, UButton
} from '#components'


const CONTACT_TYPES = [
    { label: '线上咨询', value: 'online' },
    { label: '到店咨询', value: 'in_person' }
]
const PREFERRED_CONTACT = [
    { label: '电话', value: 'phone' },
    { label: '邮箱', value: 'email' },
    { label: '视频', value: 'video' }
]
const PREFERRED_TIME = [
    { label: '上午', value: 'morning' },
    { label: '下午', value: 'afternoon' },
    { label: '晚上', value: 'evening' }
]
const VISIT_TIME = [
    { label: '上午', value: 'morning' },
    { label: '下午', value: 'afternoon' }
]
const VISIT_PURPOSE = [
    { label: '产品咨询', value: 'product' },
    { label: '项目洽谈', value: 'project' },
    { label: '售后支持', value: 'support' }
]

const form = reactive({
    contact_type: 'online',
    name: '',
    email: '',
    phone: '',
    message: '',
    preferred_contact: '',
    preferred_time: '',
    visit_date: '',
    visit_time: '',
    visit_purpose: '',
    consent: false
})

const loading = ref(false)
const successData = ref<any | null>(null)
const errorMsg = ref<string | null>(null)


const isOnline = computed(() => form.contact_type === 'online')
const isInPerson = computed(() => form.contact_type === 'in_person')

function validate(): string[] {
    const errs: string[] = []
    const emailRe = /.+@.+\..+/
    if (!form.name.trim()) errs.push('请填写姓名')
    if (!emailRe.test(form.email)) errs.push('邮箱格式不正确')
    if (!form.message.trim()) errs.push('请填写留言')
    if (!form.consent) errs.push('请勾选同意隐私政策')
    if (isOnline.value) {
        if (!form.preferred_contact) errs.push('请选择首选联络方式')
        if (!form.preferred_time) errs.push('请选择方便联系时间')
    }
    if (isInPerson.value) {
        if (!form.visit_date) errs.push('请选择到店日期')
        if (!form.visit_time) errs.push('请选择到店时段')
        if (!form.visit_purpose) errs.push('请选择到店目的')
    }
    return errs
}

const { post } = useApi()

async function handleSubmit() {
    const errs = validate()
    if (errs.length) { errorMsg.value = errs.join('；'); return }
    loading.value = true
    try {
        const payload = { ...form }
        const res = await post<any>('/api/v1/public/contacts', payload)
        successData.value = res
    } catch (e: any) {
        errorMsg.value = e?.data?.detail || e?.message || '提交失败'
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <UCard class="max-w-3xl mx-auto">
    <template #header>
      <div class="flex items-center justify-between">
        <div class="font-semibold text-lg">联系我们</div>
        <UBadge :label="isOnline ? '线上咨询' : '到店咨询'" />
      </div>
    </template>

    <div class="space-y-6">
      <!-- 联系类型 -->
      <UFormField label="联系类型" class="min-w-0">
        <USelect
          v-model="form.contact_type"
          :items="CONTACT_TYPES"
          value-key="value"
          class="w-full"
          :popper="{ strategy: 'fixed' }"
        />
      </UFormField>

      <!-- 基本信息：保持三列，但每格可收缩 -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <UFormField label="姓名 *" class="min-w-0">
          <UInput v-model="form.name" class="w-full" />
        </UFormField>

        <UFormField label="邮箱 *" class="min-w-0">
          <UInput v-model="form.email" class="w-full" />
        </UFormField>

        <UFormField label="电话（可选）" class="min-w-0">
          <UInput v-model="form.phone" class="w-full" />
        </UFormField>
      </div>

      <UFormField label="留言 *" class="min-w-0">
        <UTextarea v-model="form.message" :rows="5" class="w-full" />
      </UFormField>

      <!-- 线上咨询：两列布局，控件拉满 -->
      <div v-if="isOnline" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <UFormField label="首选联络方式 *" class="min-w-0">
          <USelect
            v-model="form.preferred_contact"
            :items="PREFERRED_CONTACT"
            value-key="value"
            class="w-full"
            :popper="{ strategy: 'fixed' }"
          />
        </UFormField>

        <UFormField label="方便联系时间 *" class="min-w-0">
          <USelect
            v-model="form.preferred_time"
            :items="PREFERRED_TIME"
            value-key="value"
            class="w-full"
            :popper="{ strategy: 'fixed' }"
          />
        </UFormField>
      </div>

      <!-- 到店咨询：保持三列，但每格可收缩且控件占满 -->
      <div v-if="isInPerson" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <UFormField label="到店日期 *" class="min-w-0">
          <UInput v-model="form.visit_date" type="date" class="w-full" />
        </UFormField>

        <UFormField label="到店时段 *" class="min-w-0">
          <USelect
            v-model="form.visit_time"
            :items="VISIT_TIME"
            value-key="value"
            class="w-full"
            :popper="{ strategy: 'fixed' }"
          />
        </UFormField>

        <UFormField label="到店目的 *" class="min-w-0">
          <USelect
            v-model="form.visit_purpose"
            :items="VISIT_PURPOSE"
            value-key="value"
            class="w-full"
            :popper="{ strategy: 'fixed' }"
          />
        </UFormField>
      </div>

      <UCheckbox v-model="form.consent" label="我已阅读并同意隐私政策 *" />

      <UAlert
        v-if="errorMsg"
        color="error"
        variant="soft"
        icon="i-lucide-alert-triangle"
        :description="errorMsg"
      />
      <UAlert
        v-if="successData"
        color="success"
        variant="soft"
        icon="i-lucide-badge-check"
        title="提交成功"
      />
    </div>

    <template #footer>
      <div class="flex justify-end">
        <UButton :loading="loading" color="primary" @click="handleSubmit">提交</UButton>
      </div>
    </template>
  </UCard>
</template>
