import HomePage from './components/HomePage.vue'
import SignIn from './components/SignIn.vue'
import OwnerSignUp from './components/OwnerSignUp.vue'
import CaretakerSignUp from './components/CaretakerSignUp.vue'
import PetInfo from './components/PetInfo.vue'
import AddPet from './components/AddPet.vue'
import FindCaretaker from './components/FindCaretaker.vue'
import OwnerInfo from './components/OwnerInfo.vue'
import CaretakerInfo from './components/CaretakerInfo.vue'
import BookingInfo from './components/BookingInfo.vue'
import AllBookingInfo from './components/AllBookingInfo.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        name: 'HomePage',
        component: HomePage,
        path: '/home'
    },
    {
        name: 'SignIn',
        component: SignIn,
        path: '/signin'
    },
    {
        name: 'OwnerSignUp',
        component: OwnerSignUp,
        path: '/owner_signup'
    },
    {
        name: 'CaretakerSignUp',
        component: CaretakerSignUp,
        path: '/caretaker_signup'
    },
    {
        name: 'PetInfo',
        component: PetInfo,
        path: '/pet_info'
    },
    {
        name: 'AddPet',
        component: AddPet,
        path: '/add_pet'
    },
    {
        name: 'FindCaretaker',
        component: FindCaretaker,
        path: '/find_caretaker'
    },
    {
        name: 'OwnerInfo',
        component: OwnerInfo,
        path: '/owner_info'
    },
    {
        name: 'CaretakerInfo',
        component: CaretakerInfo,
        path: '/caretaker_info'
    },
    {
        name: 'BookingInfo',
        component: BookingInfo,
        path: '/booking_info'
    },
    {
        name: 'AllBookingInfo',
        component: AllBookingInfo,
        path: '/all_bookings_info'
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
