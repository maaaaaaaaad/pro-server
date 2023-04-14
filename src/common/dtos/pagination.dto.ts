import { IsNumber } from 'class-validator'
import { ApiProperty } from '@nestjs/swagger'

export class PaginationInputDto {
  @IsNumber()
  @ApiProperty({
    description: 'Page count',
    default: 1,
    type: Number,
  })
  page = 1

  @IsNumber()
  @ApiProperty({
    description: 'Take size',
    default: 1,
    type: Number,
  })
  size = 1
}
