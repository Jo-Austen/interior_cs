<template>
  <div class="relative">
    <!-- 背景层：固定、全屏、铺满 -->
    <div
      class="fixed inset-0 -z-10
             bg-[url('/images/1.jpg')]
             bg-cover bg-center
             md:bg-[position:50%_40%]">
    </div>

    <!-- 可选：加一层渐变提高可读性（顶部/底部都可） -->
    <!-- <div class="fixed inset-0 -z-10 pointer-events-none
                bg-gradient-to-b from-black/30 via-transparent to-black/30">
    </div> -->

    <!-- 内容：加顶部内边距，避免被透明 Header 遮住 -->
     
    <main class="min-h-dvh pt-20 flex flex-col items-center justify-center text-center text-black">
      <h1 class="mt-12 text-5xl font-extrabold leading-tight drop-shadow">
        The smartest way to<br /> design, plan and live.
      </h1>
      <p class="mt-6 text-lg text-black/85">
        Discover modern interior solutions crafted for your space.
      </p>
      <NuxtLink
        to="site/contact"
        class="mt-8 inline-block bg-black text-white px-6 py-3 rounded-md font-medium hover:bg-gray-200 transition">
        Contact US
      </NuxtLink>
      <!-- 你其他内容… -->
    </main>
  </div>
</template>