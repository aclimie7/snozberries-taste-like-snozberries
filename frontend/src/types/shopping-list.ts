export type ShoppingItem = {
  id: string
  name: string
  quantity: number
  unit?: string
}

export type ShoppingList = {
  items: ShoppingItem[]
  zip_code: string
}
