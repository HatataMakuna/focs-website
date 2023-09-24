import { ref } from 'vue'
import { api } from 'boot/axios'
import { defineStore } from 'pinia'
import { StudChangePassword, Student } from 'src/models/student'
import { CompanyDetails, EmpChangePassword, EmpEditProfile, Employee } from 'src/models/employee'
import { AxiosError } from 'axios'
import { LocalStorage } from 'quasar'
import { Admin } from 'src/models/admin'
import { SupChangePassword, SupEditProfile, Supervisor } from 'src/models/supervisor'
import { useLocalStorageStore } from './localstorage-store'

export const useStore = defineStore('user', () => {
  const loggingInStudent = ref(false)
  const loginError = ref(false)
  const errorMessage = ref('')
  const lsStore = useLocalStorageStore()


  async function logInStudent(value: Student) {
    try {
      loggingInStudent.value = true
      const resp = await api.post('/user/login-stud', value)

      // Check the response status code
      if (resp.status === 200) {
        // if login successful
        loginError.value = false
        lsStore.setIsAuthenticated(true)
        lsStore.setAuthUserType('stud')
        lsStore.setUsername(value.student_id)
      }
      loggingInStudent.value = false
    } catch (error) {
      const errorMsg = error as AxiosError
      //console.log('Login error:', errorMsg)
      loginError.value = true
      errorMessage.value = (errorMsg.response?.data as { message: string }).message
      lsStore.setIsAuthenticated(false)
      lsStore.setAuthUserType('none')
      lsStore.setUsername('none')
    }
  }

})

