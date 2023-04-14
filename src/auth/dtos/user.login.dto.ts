import { PickType } from '@nestjs/swagger'
import { UserEntity } from '../entities/user.entity'
import { CoreOutputDto } from '../../common/dtos/core.output.dto'

export class UserLoginInputDto extends PickType(UserEntity, [
  'email',
  'password',
]) {}

export type UserLoginOutputDto = CoreOutputDto & {
  token?: string
}
