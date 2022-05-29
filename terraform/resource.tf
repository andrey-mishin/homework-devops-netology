resource "yandex_compute_instance" "ubuntu-vm" {
  name = "ubuntu-vm"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "${var.ubuntu-20-04}"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.default.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/yc-test.pub")}"
  }
}
