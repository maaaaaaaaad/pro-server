import { CoreOutputDto } from '../../common/dtos/core.output.dto'
import { CategoryEntity } from '../entities/category.entity'

export type CategoriesGetOutputDto = CoreOutputDto & {
  categories?: CategoryEntity[]
}
