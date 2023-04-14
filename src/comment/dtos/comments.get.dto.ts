import { ApiProperty } from '@nestjs/swagger'
import { PaginationInputDto } from '../../common/dtos/pagination.dto'

export class CommentsGetInputDto extends PaginationInputDto {
  @ApiProperty({
    description: 'Item primary key',
    type: Number,
    nullable: false,
    required: true,
  })
  itemId: number
}
