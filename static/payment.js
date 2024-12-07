const fieldTipeBayar = document.querySelector(".tipe-bayar")
const tipeItem = document.querySelectorAll(".tipe-item") 

fieldTipeBayar.querySelectorAll("input[type='radio']").forEach(item => {
	item.addEventListener("change", ev => {
		if(ev.currentTarget.checked) {
			tipeItem.forEach(ix => {
				if(
					ix.classList.contains(ev.currentTarget.value) && 
					!ix.classList.contains("active")
				) {
					ix.classList.add("active")
				} else ix.classList.remove("active")
			})
		}
	})
})
