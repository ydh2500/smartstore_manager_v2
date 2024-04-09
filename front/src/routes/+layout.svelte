
<style>
  nav ul {
    display: flex;
    gap: 40px; /* 원하는 간격을 설정하세요 */
    list-style-type: none; /* 이 부분을 추가합니다 */
  }
</style>


<div class = "container">
    <nav>
        <ul>
            <li><a href = "/">Home</a></li>
            <li><a href = "/product_orders">Orders</a></li>
            <li><a href = "about">About</a></li>

        </ul>
    </nav>

    <slot />
</div>